from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from taggit.managers import TaggableManager
from datalink.models import User, UserForm, LoginForm
from representative.models import Representative, RepresentativeForm
from post.models import Post
from network.models import Network
from django.contrib.auth.decorators import login_required
import thread
import json




#-------------------------------------------------------------Important Functions--------------------------------------------
def send_push(final_list, data, owner_email):
	f = open('logp.txt','w+')
	for i in final_list:	
		f.write(i+"\n")
	f.close()

def collect_push(email, tags, data, post):
	"""
	This function returns a list of email of all the users eligible to view the post
	Since this function runs in a thread, it needs to be memory efficient. There'll be too many instances of 
	this function running at the same time.
	"""
	users = User.objects.filter(network=User.objects.get(email=email).network)	#List of all users belonging to the network of owner
	ids = [x.id for x in users] #Getting the list of ids of the users to lower data load on RAM
	del users
	final = []
	for i in ids:	#Iterating over users and tags to match the tags of post with the tags of users
		temp = User.objects.get(id=i)
		for j in tags:
			if j.lower() in temp.tags.names():
				final.append(temp.email)
	final = list(set(final))	#Final list of eligible users
	del ids
	if email in final:
		final.remove(email)
	for i in final:
		post.viewers.add(User.objects.get(email=i))
	send_push(final,data, email)

#----------------------------------------------------------Views-----------------------------------------------------

@cache_page(60*15)
def home(request):
	return render(request,'home.html')

@login_required
def profile(request):
	user = User.objects.get(mainuser=request.user)
	data = {}
	data['first_name'] = user.first_name
	data['last_name'] = user.last_name
	data['name'] = user.first_name + " " + user.last_name
	data['email'] = user.email
	data['mobile'] = user.mobile
	data['raw_tags'] = ", ".join(user.tags.names())
	data['tags'] = ", ".join([i.title() for i in user.tags.names()])
	data['network'] = user.network
	data['max_notification'] = user.max_notification
	data['todays_notification_count'] = user.todays_notification_count
	posts = cache.get('posts'+user.network.name)
	if posts==None:
		posts = Post.objects.filter(network=user.network)
		cache.set('posts'+user.network.name,posts)
	finalposts = []
	count = 0
	for i in posts:
		if user == i.owner:
			count+=1
	data['total_posts'] = count
	return render(request, 'profile.html', data)

@login_required
def feed(request):
	user = User.objects.get(mainuser=request.user)
	posts = cache.get('posts')
	if posts==None:
		posts = Post.objects.filter(network=user.network)
		cache.set('posts',posts)
	finalposts = []
	for i in posts:
		if user in i.viewers.all():
			finalposts.append(i.data + "  -  "+ i.owner.first_name + " " + i.owner.last_name)
	if len(finalposts)==0:
		nofeeds = True
	else:
		nofeeds = False
	return render(request,'feed.html',{'posts':finalposts,'nofeeds':nofeeds})



@login_required
def post(request,data):
	email = User.objects.get(mainuser=request.user).email
	newPost = Post(data=data, owner=User.objects.get(email=email), push_sent=False, network=User.objects.get(mainuser=request.user).network)
	newPost.save()
	tags = data.split(" ")
	thread.start_new_thread(collect_push, (email, tags, data, newPost))
	return HttpResponse(email+" " + " ".join(tags))


@login_required
def signup_user(request):
	if request.method == 'POST':
		form = UserForm(request.POST.copy())
		form.data["mainuser"] = request.user.id
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/feed/')
		else:
			return HttpResponse(form.errors)
			return render(request, 'sign_up.html', {'form': form, 'type':'User'})
	else:
		try:
			user = User.objects.get(mainuser = request.user)
			return HttpResponseRedirect("/feed/")
		except User.DoesNotExist:
			form = UserForm()
			return render(request, 'sign_up.html', {'form': form, 'type':'User'})

@login_required
def signup_rep(request):
	if request.method == 'POST':
		form = RepresentativeForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/feed/')
		else:
			form = RepresentativeForm()
			return render(request, 'sign_up.html', {'form': form, 'type':'Representative'})
	else:
		form = RepresentativeForm()
		return render(request, 'sign_up.html', {'form': form, 'type':'Representative'})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = auth.authenticate(username=request.POST['username'],password=request.POST['password1'])
            auth.login(request, new_user)
            return HttpResponseRedirect("/signup/user/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form,})

@login_required
def trending_tags(request, id):
	from collections import Counter
	network = Network.objects.get(id=id)
	tags = cache.get('famous_tags_'+network.name)
	slugs = cache.get('famous_slugs_'+network.name)
	if tags==None or slugs==None:
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
	return HttpResponse(json.dumps({'tags':tags[:20],'slugs':slugs[:20]}))

def pagenotfound(request):
	url = request.build_absolute_uri(request.get_full_path())
	return render(request, '404.html',{'url':url})