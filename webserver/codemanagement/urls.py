from django.conf.urls.defaults import patterns, url, include

from .views import CreateRepoView


urlpatterns = patterns(
    "",

    url(r'^competition/(?P<comp_slug>[\w-]+)/create-repo/$',
        CreateRepoView.as_view(),
        name='create_repo'),

    url(r'^repo/', include('greta.repo_view_urls')),
)
