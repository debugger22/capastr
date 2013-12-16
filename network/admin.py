from django.contrib import admin
from network.models import Network

class NetworkAdmin(admin.ModelAdmin):
	list_display = ('name' , 'city', 'country')
	list_filter = ('city', 'state')
	search_fields = ('name',)

admin.site.register(Network, NetworkAdmin)