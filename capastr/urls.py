from django.conf.urls import patterns, include, url
import settings
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'capastr.views.home', name='home'),
    url(r'^feed/$', 'capastr.views.feed', name='feed'),

    url(r'^register/$', 'capastr.views.register', name='register'),
    url(r'^post/email/(.*)/data/(.*)/$', 'capastr.views.post', name='post'),
    url(r'^signup/user/$', 'capastr.views.signup_user', name='signup_user'),
    url(r'^signup/user/success/$', 'capastr.views.signup_user_success', name='signup_user_success'),
    url(r'^signup/rep/$', 'capastr.views.signup_rep', name='signup_rep'),
    url(r'^signup/rep/success/$', 'capastr.views.signup_rep_success', name='signup_rep_success'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^register/user/$', 'capastr.views.register_user', name='register_user'),

    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if 'datalink' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        #url(r'^data/', include('datalink.urls')),
    )
