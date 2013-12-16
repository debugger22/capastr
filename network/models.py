from django.db import models
from django.forms import ModelForm

class Network(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	zip = models.CharField(max_length=7)

	def __unicode__(self):
		return self.name

class NetworkForm(ModelForm):
	class Meta:
		model = Network
