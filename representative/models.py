from django.db import models
from django.forms import ModelForm
from django import forms
from taggit.managers import TaggableManager
from network.models import Network


class Representative(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)
    mobile = models.CharField(max_length=13)
    password = models.CharField(max_length=50)
    network = models.ForeignKey(Network, related_name='+')
    time = models.DateField(auto_now_add=True)
    def __unicode__(self):
    	return self.first_name + " " + self.last_name + ", " + self.email

class RepresentativeForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Representative
