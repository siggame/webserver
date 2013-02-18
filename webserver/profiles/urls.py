from django.conf.urls.defaults import patterns, url

from webserver.accounts.views import (ProfileListView, ProfileView,
                                      MyProfileView, ProfileUpdateView)
from webserver.accounts.forms import LoginForm


urlpatterns = patterns(
    '',
    # Authentication
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html',
         'authentication_form': LoginForm},
        name='login'),

    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),

    # Profiles
    url(r'^profiles/$',
        ProfileListView.as_view(),
        name="list_profile"),

    url(r'^profile/$',
        MyProfileView.as_view(),
        name="view_profile"),

    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$',
        ProfileView.as_view(),
        name="view_profile"),

    url(r'^profile-edit/$',
        ProfileUpdateView.as_view(),
        name="update_profile"),
)
