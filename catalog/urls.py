from django.conf.urls.defaults import *

urlpatterns = patterns('cinemania.catalog.views',
    (r'^manager/$', 'index'),                   # Welcome page for managers
    (r'^manager/login', 'manager_login'),       # Login page
)
