from django.conf.urls import patterns, url

from .views import (ProfileListView, ProfileView,
                    MyProfileView, ProfileUpdateView)


urlpatterns = patterns(
    '',
    # Profiles
    url(r'^profiles/$',
        ProfileListView.as_view(),
        name="list_profile"),

    url(r'^profile/$',
        MyProfileView.as_view(),
        name="view_profile"),

    url(r'^profile/(?P<username>.+)/$',
        ProfileView.as_view(),
        name="view_profile"),

    url(r'^profile-edit/$',
        ProfileUpdateView.as_view(),
        name="update_profile"),
)
