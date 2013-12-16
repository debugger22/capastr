from django.db import models
from django.forms import ModelForm
from taggit.managers import TaggableManager
from datalink.models import User

class Post(models.Model):
    data = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='+')
    viewers = models.ManyToManyField(User, related_name='+', blank=True)
    push_sent = models.BooleanField()
    time = models.DateField(auto_now_add=True)

    def __unicode__(self):
    	return self.data +"::"+ self.owner.email 