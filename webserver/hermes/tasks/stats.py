from celery import task
from django.db.models import F

from competition.models import Competition
from ..models import TeamStats

import logging

logger = logging.getLogger(__name__)


def get_team_stats(team):
    results = []
    opponents = team.competition.team_set.exclude(pk=team.pk)
    for opponent in opponents.order_by('slug'):
        team_scores = team.gamescore_set.filter(game__scores__team=opponent)
        results.append({
            'name': opponent.name,
            'n_games': team_scores.count(),
            'n_win': team_scores.filter(score=1).count(),
            'n_loss': team_scores.filter(score=0).count(),
        })
    return results



@task()
def update_game_stats(competition_slug):
    try:
        competition = Competition.objects.get(slug=competition_slug)
    except Competition.DoesNotExist:
        logger.error("Cannot locate competition {}".format(competition_slug))

    teams = competition.team_set.all()

    for team in teams:
        stats, _ = TeamStats.objects.get_or_create(team=team)

        scores = team.gamescore_set.all()
        wins = scores.filter(score=1).count()
        losses = scores.filter(score=0).count()

        stats.data = {
            'teams': get_team_stats(team),
            'total': {
                'n_games': scores.count(),
                'n_win': wins,
                'n_loss': losses,
                'ratio': float(wins) / float(losses)
            }
        }
        stats.save()
