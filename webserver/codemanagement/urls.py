from django.conf.urls import patterns, url, include
from piston.resource import Resource

from .views import (CreateRepoView, UpdatePasswordView,
                    ListSubmissionView, SubmitView)
from .api_handlers import RepoAuthHandler, RepoPathHandler, RepoTagListHandler


urlpatterns = patterns(
    "",

    url(r'^api/repo/auth/', Resource(handler=RepoAuthHandler)),
    url(r'^api/repo/path/', Resource(handler=RepoPathHandler)),
    url(r'^api/repo/tags/', Resource(handler=RepoTagListHandler)),

    url(r'^competition/(?P<comp_slug>[\w-]+)/create-repo/$',
        CreateRepoView.as_view(),
        name='create_repo'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/update-password/$',
        UpdatePasswordView.as_view(),
        name='update_repo_password'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/submissions/$',
        ListSubmissionView.as_view(),
        name='list_submissions'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/submit/(?P<sha>[a-f0-9]{40})/$',
        SubmitView.as_view(),
        name='submit'),

    url(r'^repo/', include('greta.repo_view_urls')),
)
