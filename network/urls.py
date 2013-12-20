from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from views import *

urlpatterns = patterns('',
	url(r'^(\d+)/$', view_network, name='view_network'),
	#url(r'^networks/(\d+)/location/$', location, name='location'),
)