from django.db import models
from django.forms import ModelForm
from taggit.managers import TaggableManager
from django import forms
from network.models import Network
from django.contrib.auth.models import User as MainUser

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)
    mobile = models.CharField(max_length=13)
    network = models.ForeignKey(Network, related_name='+')
    tags = TaggableManager()
    max_notification = models.PositiveSmallIntegerField(verbose_name="Max Notifications",\
    	error_messages = {'null':'Please enter a value','blank':'Please enter a value','invalid':'Please enter a numeric value'},\
    	help_text="Max no. of notifications on your phone.")
    todays_notification_count = models.PositiveSmallIntegerField(verbose_name="Today's Notifications count", blank=True, null=True)
    mainuser = models.ForeignKey(MainUser, related_name='+', blank=True, null=True ,verbose_name="Django's User Model Object")
    time = models.DateField(auto_now_add=True)
    def __unicode__(self):
    	return self.first_name + " " + self.last_name + ", " + self.email

class UserForm(ModelForm):
	class Meta:
		model = User


class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())