from django.shortcuts import render
from django.contrib import auth
from django.core.cache import cache
from datalink.models import User
from representative.models import Representative, RepresentativeForm
from post.models import Post
from network.models import Network
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404

@login_required
def view_network(request,id):
	try:
		network = Network.objects.get(id=int(id))
	except Network.DoesNotExist:
		raise Http404
	address = network.address + ", " + network.city + ", " + network.state
	tags = cache.get('famous_tags_'+network.name)
	slugs = cache.get('famous_slugs_'+network.name)	
	if tags==None:
		from collections import Counter
		users = cache.get('users_'+network.name)
		if users==None:
			users = User.objects.filter(network=network)
			cache.set('users_'+network.name,users,60*60*12)
		tags = []
		slugs = []
		for i in users:
			tags += i.tags.names()
			slugs += i.tags.slugs()
		temp_tags = Counter(tags).most_common()
		temp_slugs = Counter(slugs).most_common()
		tags = []
		slugs = []
		for i in xrange(len(temp_tags)):
			tags.append(temp_tags[i][0])
			slugs.append(temp_slugs[i][0])
		cache.set('famous_tags_'+network.name,tags,60*60*6)
		cache.set('famous_slugs_'+network.name,slugs,60*60*6)

	users = cache.get('users_'+network.name)
	if users==None:
		users = User.objects.filter(network=network)
		cache.set('users_'+network.name,users,60*60*12)
	return render(request,'network.html',{'users':users,'tags':tags[:100], 'slugs':slugs[:100],'network':network,'address':address})