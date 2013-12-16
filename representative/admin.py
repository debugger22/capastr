from django.contrib import admin
from representative.models import Representative

class RepresentativeAdmin(admin.ModelAdmin):
	list_display = ('first_name' , 'last_name', 'network')
	list_filter = ('network',)
	search_fields = ('name',)

admin.site.register(Representative, RepresentativeAdmin)