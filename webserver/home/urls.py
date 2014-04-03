from django.conf.urls import patterns, url

from views import HomePageView, DocsPageView


urlpatterns = patterns(
    '',
    url(r'^$',
        HomePageView.as_view(),
        name='home'),
    url(r'^docs/$',
        DocsPageView.as_view(),
        name="docs"),
)
