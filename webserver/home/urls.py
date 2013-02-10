from django.conf.urls.defaults import patterns, url

from views import HomePageView


urlpatterns = patterns(
    '',
    url(r'^$',
        HomePageView.as_view(),
        name='home'),
)
