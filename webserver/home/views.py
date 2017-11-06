from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from competition.models import Competition

from datetime import datetime
from time import mktime

import feedparser


class FeedException(Exception):
    pass


class HomePageView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        context["open_competitions"] = Competition.objects.filter(is_open=True)
        context["running_competitions"] = Competition.objects.filter(is_running=True)
        context["next_competition"] = Competition.objects.first()

        if not self.request.user.is_anonymous():
            my_competitions = Competition.objects.user_registered(self.request.user)
            context["registered_competitions"] = my_competitions.exclude(is_running=False, is_open=False)
            context["closed_competitions"] = my_competitions.filter(is_running=False, is_open=False)
        return context

    def get_template_names(self):
        if self.request.user.is_anonymous():
            return ['home/unauthenticated.html']
        return ['home/authenticated.html']


class FeedAPIView(APIView):
    """List feed posts

    """
    feed_url = None
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """Ping an atom feed and get the latest posts"""

        if self.feed_url is None:
            raise FeedException("feed_url not set")

        feed = feedparser.parse(self.feed_url)

        entries = feed['entries']

        result = []
        for entry in entries:
            result.append({
                'title': entry['title'],
                'date': datetime.fromtimestamp(mktime(entry['published_parsed'])),
                'post': entry['summary'],
                'links': [l['href'] for l in entry['links']] ,
                'category': entry.get('category', None),
                'tag': entry.get('tag', None)
            })
        return Response(result)


class BlogFeedAPIView(FeedAPIView):
    """List blog posts

    """
    feed_url = 'http://siggame.io/feed.xml'


class StatusFeedAPIView(FeedAPIView):
    """List status posts

    """
    feed_url = 'http://status.megaminerai.com/feed.xml'
