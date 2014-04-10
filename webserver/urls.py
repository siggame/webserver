from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.contrib.flatpages.views import flatpage
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView


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
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/', include('allauth.urls')),

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
        url(r'^qr/(?P<path>.*\.png)$', 'django.views.static.serve',
            {'document_root': settings.QR_DIR}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^500/$', TemplateView.as_view(template_name="500.html")),
        url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    )

# Flat pages
urlpatterns += patterns(
    '',
    # Cache flat pages for 60 seconds
    url(r'^(?P<url>.*/)$', cache_page(settings.FLATPAGE_TIMEOUT)(flatpage)),
)
