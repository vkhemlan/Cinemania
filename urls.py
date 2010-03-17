from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/vkhemlan/django-projects/cinemania/static/'}),
    (r'^catalog/', include('cinemania.catalog.urls')),
    (r'^admin/', include(admin.site.urls)),
)
