from django.conf.urls import patterns, url, include

from .views import (CreateRepoView, UpdatePasswordView,
                    ListSubmissionView, SubmitView)
from .api import RepoAuth, RepoPath, RepoTagList


urlpatterns = patterns(
    "",

    url(r'^api/repo/auth/', RepoAuth.as_view()),
    url(r'^api/repo/path/(?P<team_id>[\d]+)/$', RepoPath.as_view()),
    url(r'^api/repo/tags/(?P<competition_slug>[\w-]+)/$', RepoTagList.as_view()),

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
