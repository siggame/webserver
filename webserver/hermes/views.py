from django.views.generic.detail import DetailView

from competition.views.game_views import GameView
from .models import TeamStats

import logging

logger = logging.getLogger(__name__)


class GameStatsView(GameView, DetailView):
    template_name = 'hermes/game_stats.html'
    context_object_name = 'stats'

    def get_object(self):
        self.team = self.get_team()
        stats, _ = TeamStats.objects.get_or_create(team=self.team)
        return stats
