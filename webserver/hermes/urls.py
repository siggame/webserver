from django.conf.urls.defaults import patterns, url

from .views import GameStatsView

urlpatterns = patterns(
    '',
    url(r'^competition/(?P<comp_slug>[\w-]+)/gamestats/$',
        GameStatsView.as_view(),
        name='game_stats'),
)
