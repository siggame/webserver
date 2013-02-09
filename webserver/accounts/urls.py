from django.conf.urls.defaults import patterns, url

from webserver.accounts.views import (ProfileListView, ProfileView,
                                      ProfileUpdateView)


urlpatterns = patterns(
    '',
    url(r'^profiles/$',
        ProfileListView.as_view(),
        name="list_profile"),

    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$',
        ProfileView.as_view(),
        name="view_profile"),

    url(r'^profile-edit/$',
        ProfileUpdateView.as_view(),
        name="update_profile"),
)
