from cinemania.catalog.models import *
from django.contrib import admin

# Let Django make an admin page for all tables in the database

admin.site.register(Movie)
admin.site.register(Room)
admin.site.register(Showing)
admin.site.register(ShowingInstance)
admin.site.register(Customer)
admin.site.register(Reserve)
admin.site.register(Order)
admin.site.register(AdminUser)
