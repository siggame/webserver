from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import logout_then_login
from django.conf import settings
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    # Webserver urls
    url(r'^', include('webserver.home.urls')),
    url(r'^', include('webserver.profiles.urls')),
    url(r'^', include('webserver.codemanagement.urls')),
    url(r'^', include('webserver.hermes.urls')),

    # Competition
    url(r'^', include('competition.urls')),

    # Custom Auth for Login
    url(r'^accounts/auth/$', 'webserver.views.auth_view'),

    # Django AllAuth
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/', include('allauth.urls')),

    # Zinnia Blog
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,'show_indexes':True}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^500/$', 'django.views.generic.simple.direct_to_template',
            {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template',
            {'template': '404.html'}),
    )

# Flat pages
urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^(?P<url>.*)$', 'flatpage'),
)
