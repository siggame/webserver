from celery import task
from django.db.models import F

from competition.models import Competition, GameScore
from ..models import TeamStats

import functools
import itertools
import logging

from elopopulars import FIDERating, make_fide_k_factor
from elo import Elo
from trueskill import TrueSkill, Rating, rate_1vs1

logger = logging.getLogger(__name__)


def get_team_stats(team):
    results = []
    opponents = team.competition.team_set.exclude(pk=team.pk)
    for opponent in opponents.order_by('slug'):
        team_scores = team.gamescore_set.filter(game__scores__team=opponent,
                                                game__status="Complete")
        results.append({
            'name': opponent.name,
            'n_games': team_scores.count(),
            'n_win': team_scores.filter(score=1).count(),
            'n_loss': team_scores.filter(score=0).count(),
        })
    return results


def get_version_stats(team):
    results = {}
    scores = team.gamescore_set.filter(game__status="Complete")
    for score in scores:
        version = score.data['version']
        wins = score.score
        losses = 1 - score.score
        try:
            results[version]['n_games'] += 1
            results[version]['n_win'] += wins
            results[version]['n_loss'] += losses
        except KeyError:
            results[version] = {
                'version': version,
                'n_games': 1,
                'n_win': wins,
                'n_loss': losses
            }
    return results.values()


def calculate_rating(competition, rating_class, rating_function):
    games = competition.game_set.filter(status__iexact="complete")
    ratings = {t.pk: rating_class() for t in competition.team_set.all()}

    for game in games:
        draw = False

        try:
            # Try to determine a winner and a loser
            winner = game.scores.get(score=1).team
            loser = game.scores.get(score=0).team
        except GameScore.DoesNotExist:
            draw = True

        try:
            # If it's drawn, just unpack the list
            if draw:
                winner, loser = list(game.teams.all())
        except ValueError:
            logger.debug("Unable to unpack results. Team must have been deleted")
            continue

        ratings[winner.pk], ratings[loser.pk] = rating_function(ratings[winner.pk], ratings[loser.pk], drawn=draw)

    return ratings


def calculate_elo(competition):
    fide30 = Elo(make_fide_k_factor(30, 15, 10), FIDERating)
    return calculate_rating(competition, FIDERating, fide30.rate_1vs1)


def calculate_trueskill(competition):
    trueskill = TrueSkill()
    rating_func = functools.partial(rate_1vs1, env=trueskill)
    return calculate_rating(competition, Rating, rating_func)


@task()
def update_game_stats(competition_slug):
    try:
        competition = Competition.objects.get(slug=competition_slug)
    except Competition.DoesNotExist:
        logger.error("Cannot locate competition {}".format(competition_slug))

    elos = calculate_elo(competition)
    ts_ratings = calculate_trueskill(competition)

    teams = competition.team_set.all()

    for team in teams:
        stats, _ = TeamStats.objects.get_or_create(team=team)

        scores = team.gamescore_set.filter(game__status__iexact="complete")

        if not scores.exists():
            continue

        wins = scores.filter(score=1).count()
        losses = scores.filter(score=0).count()

        stats.data = {
            'ratings': {
                'elo': float(elos[team.pk]),
                'trueskill': float(ts_ratings[team.pk])
            },
            'teams': get_team_stats(team),
            'versions': get_version_stats(team),
            'total': {
                'n_games': scores.count(),
                'n_win': wins,
                'n_loss': losses,
                'ratio': float(wins) / float(losses)
            }
        }
        stats.save()
