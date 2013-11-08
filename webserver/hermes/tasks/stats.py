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
def calculate_win_loss_ratios(competition_slug):
    try:
        competition = Competition.objects.get(slug=competition_slug)
    except Competition.DoesNotExist:
        logger.error("Cannot locate competition {}".format(competition_slug))

    teams = competition.team_set.all()

    for team in teams:
        scores = team.gamescore_set.all()
        stats, _ = TeamStats.objects.get_or_create(team=team)
        stats.data = {
            'teams': get_team_stats(team),
            'total': {
                'n_games': scores.count(),
                'n_win': scores.filter(score=1).count(),
                'n_loss': scores.filter(score=0).count(),
            }
        }
        stats.save()
