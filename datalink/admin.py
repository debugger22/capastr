from django.contrib import admin

from datalink.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'network')
    list_filter = ('time', 'network')
    search_fields = ('first_name', 'last_name', 'email' ,'mobile', 'network')

admin.site.register(User, UserAdmin)