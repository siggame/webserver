from django.conf.urls.defaults import patterns, url, include
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

    # Django AllAuth
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
    )

# Flat pages
urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^(?P<url>.*)$', 'flatpage'),
)
