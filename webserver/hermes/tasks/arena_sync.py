from celery import task
from datetime import datetime, timedelta
from django.db.models import Q

from competition.models.competition_model import Competition
from competition.models.game_model import Game, GameScore
from competition.models.team_model import Team

from .stats import update_game_stats

import slumber
import logging
import random
import requests
import json


logger = logging.getLogger(__name__)

SCHEDULED_STRING = "Scheduled"
COMPLETED_STRING = "Complete"
RUNNING_STRING = "Running"
FAILED_STRING = "Failed"
BUILDING_STRING = "Building"
NEW_STRING = "New"
HAS_STARTED = [COMPLETED_STRING, RUNNING_STRING, FAILED_STRING, BUILDING_STRING]
HAS_FINISHED = [COMPLETED_STRING, FAILED_STRING]
HAS_NOT_FINISHED = [NEW_STRING, SCHEDULED_STRING, RUNNING_STRING, BUILDING_STRING]


@task()
def create_test_game(competition):
    game_data = {
        'gamelog_url': 'http://placekitten.com/g/200/300',
        'api_url': 'http://placekitten.com/g/300/200',
        }
    score_data = {
        'output_url': 'http://placekitten.com/g/300/300',
        'version': 'test_game',
        }
    teams = list(competition.team_set.all())
    players = random.sample(teams, 2)

    g  = Game.objects.create(competition=competition,
                             extra_data=json.dumps(game_data))
    for player in players:
        GameScore.objects.create(game=g, team=player,
                                 score=random.randint(0,1),
                                 extra_data=json.dumps(score_data))
    p1, p2 = players
    logger.info("Created game {} between {} and {}".format(str(g), p1, p2))


def populate_score(api, competition, game=None):
    # Fetch the team object based on the slug of the team name

    try:
        team = Team.objects.get(competition=competition,
                                slug=api["name"]["name"])
    except Team.DoesNotExist:
        team = Team.objects.get(competition=competition,
                                name=api["name"]["name"])

    # There is no game object provided, create a new gamescore
    if game == None:
        score = GameScore()
        score.team = team
    # Or look up an old one
    else:
        # Apparently we can catch a game where there is only one team, when
        # in reality, there are two.
        score, _ = GameScore.objects.get_or_create(game=game, team=team)

    # If the team won the game give them a point
    if api["won"] == True:
        score.score = 1
    #: Not set to false if a team loses, as it turns out.
    elif api["output_url"]:
        score.score = 0
    else:
        score.score = None

    # Set extra data for the glog by saving the game_data dict
    # returned by the API
    extra = score.data
    try:
        extra.update(api)
    except AttributeError:
        extra = api

    score.extra_data = json.dumps(extra)
    return score


@task()
def fetch_games(arena_api_url, competition_slug,
                offset=0, at_a_time=60, max_to_fetch=100000, max_time=None):
    # Fetch a bunch of games
    competition = Competition.objects.get(slug=competition_slug)
    start_time = datetime.today()
    found_one_new = True
    for load in xrange(offset, max_to_fetch, at_a_time):
        #If we go through a whole page without a new game being found, quit.
        if found_one_new == False:
            break
        found_one_new = False
        if max_time != None and datetime.today()-start_time > timedelta(seconds=max_time):
            break
        # Query the arena api
        api = slumber.API(arena_api_url)
        try:
            obj = api.game.get(offset=load, limit=at_a_time)
        except requests.ConnectionError:
            logger.error("Cannot connect to arena at {}".format(arena_api_url))
            return

        if len(obj["objects"]) == 0:
            break
        print "Loading offset {}".format(load)
        for game in obj["objects"]:
            scores = []
            # Populate a score object for this match
            try:
                for team in game["game_data"]:
                    score = populate_score(team, competition, None)
                    scores.append(score)
            # Handle if the team cannot be found.
            except Team.DoesNotExist:
                print "Could not find team: {}".format(team["name"]["name"])
                continue

            # Try to load or create a game object using get_or_create
            status = game['status']
            extra = game
            extra.update({'api_url': arena_api_url})
            defaults = {
                'start_time': datetime.today() if status in HAS_STARTED else None,
                'end_time': datetime.today() if status in HAS_FINISHED else None,
                'status': status,
                'extra_data': json.dumps(extra),
            }
            x, c = Game.objects.get_or_create(game_id=game["id"],
                                              competition=competition,
                                              defaults=defaults)
            found_one_new = found_one_new or c

            # If the object is created, then save it and the related
            # score objecs
            if c:
                x.save()
                for score in scores:
                    score.game = x
                    score.save()


@task()
def update_games(arena_api_url, competition_slug,
                 offset=0, at_a_time=20, max_updates=10000, max_time=None):
    competition = Competition.objects.get(slug=competition_slug)

    # Start an empty object
    q_filter = None
    # For every status type that indicates the game ended
    for status in HAS_NOT_FINISHED:
        # Or the two status types together
        t = Q(status=status)
        if q_filter != None:
            q_filter = q_filter | t
        else:
            q_filter = t

    start_time = datetime.today()
    for load in xrange(offset, max_updates, at_a_time):
        if max_time != None and datetime.today()-start_time > timedelta(seconds=max_time):
            break
        # Load all the games that haven't marked as finished (using the filter)
        unfinished_games = Game.objects.filter(q_filter)
        unfinished_games = unfinished_games.filter(competition=competition)
        unfinished_games = unfinished_games.order_by('-pk')[load:load+at_a_time]

        api = slumber.API(arena_api_url)

        for game in unfinished_games:
            # Query the api
            try:
                obj = api.game(game.game_id).get()
            except slumber.exceptions.HttpClientError:
                logger.info("Cannot fetch game {}".format(game.id))
                continue
            except requests.ConnectionError:
                logger.error("Cannot connect to arena at {}".format(arena_api_url))
                return

            scores = []
            status = obj["status"]
            # See if the game status is changed
            if status != game.status:
                # Populate new score objects from the server
                for team in obj["game_data"]:
                    score = populate_score(team, competition, game)
                    scores.append(score)
                # If we haven't recorded a start time, see if we should.
                if game.start_time == None:
                    game.start_time = datetime.today() if status in HAS_STARTED+HAS_FINISHED else None
                # Same for the end time.
                if game.end_time == None:
                    game.end_time = datetime.today() if status in HAS_FINISHED else None

                # Save API data
                data = game.data
                data.update(obj)
                data.update({'api_url': arena_api_url})
                game.extra_data = json.dumps(data)
                game.status = status

                game.save()     # Save the Game

                # Update the related score objects
                for score in scores:
                    score.save()
