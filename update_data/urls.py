from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from views import *

urlpatterns = patterns('',

	url(r'^name/$', name, name='home'),
	url(r'^email/$', email, name='email'),
	url(r'^mobile/$', mobile, name='mobile'),
	url(r'^tags/$', tags, name='tags'),
)