from django.conf.urls import patterns, url

from views import HomePageView, BlogFeedAPIView, StatusFeedAPIView


urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^api/blog-feed/$', BlogFeedAPIView.as_view(), name='blog-feed'),
    url(r'^api/status-feed/$', StatusFeedAPIView.as_view(), name='status-feed'),
)
