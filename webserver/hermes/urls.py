from django.conf.urls.defaults import patterns, url
from .views import rating

urlpatterns = patterns(
    '',
    url(r'^rating/$', rating, name="arena_rating")
)
