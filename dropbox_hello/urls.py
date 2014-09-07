from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^start_auth', 'dropbox_hello.views.start_auth', name='start_auth'),
    url(r'^end_auth', 'dropbox_hello.views.end_auth', name='end_auth'),
    url(r'^', 'dropbox_hello.views.home', name='home'),
)
