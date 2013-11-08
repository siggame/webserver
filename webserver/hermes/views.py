from django.views.generic.base import TemplateView

from competition.views.mixins import CompetitionViewMixin, RequireRunningMixin

import logging

logger = logging.getLogger(__name__)


class GameStatsView(CompetitionViewMixin, RequireRunningMixin, TemplateView):
    template_name = 'hermes/game_stats.html'
