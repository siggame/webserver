from django.conf.urls.defaults import patterns, url, include
from piston.resource import Resource

from .views import CreateRepoView, UpdatePasswordView
from .api_handlers import RepoAuthHandler


urlpatterns = patterns(
    "",

    url(r'^api/repo/auth/', Resource(handler=RepoAuthHandler)),

    url(r'^competition/(?P<comp_slug>[\w-]+)/create-repo/$',
        CreateRepoView.as_view(),
        name='create_repo'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/update-password/$',
        UpdatePasswordView.as_view(),
        name='update_repo_password'),

    url(r'^repo/', include('greta.repo_view_urls')),
)
