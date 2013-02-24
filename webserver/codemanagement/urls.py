from django.conf.urls.defaults import patterns, url, include

from .views import CreateRepoView, UpdatePasswordView


urlpatterns = patterns(
    "",

    url(r'^competition/(?P<comp_slug>[\w-]+)/create-repo/$',
        CreateRepoView.as_view(),
        name='create_repo'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/update-password/$',
        UpdatePasswordView.as_view(),
        name='update_repo_password'),

    url(r'^repo/', include('greta.repo_view_urls')),
)
