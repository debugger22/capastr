from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from taggit.managers import TaggableManager
from datalink.models import User, UserForm, LoginForm
from representative.models import Representative, RepresentativeForm
from post.models import Post
from django.contrib.auth.decorators import login_required
import thread


def home(request):
	return render(request,'home.html')


@login_required
def feed(request):
	user = User.objects.get(mainuser=request.user)
	posts = Post.objects.filter(network=user.network)
	finalposts = []
	for i in posts:
		if user in i.viewers.all():
			finalposts.append(i.data)
	return HttpResponse("<br/>".join(finalposts))

def register(request):
	newUser = UserForm(request.GET)
	if newUser.is_valid():
		newUser.save()
		return HttpResponse(1)
	else:
		return HttpResponse(0)


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
			if j in temp.tags.names():
				final.append(temp.email)
	final = list(set(final))	#Final list of eligible users
	del ids
	if email in final:
		final.remove(email)
	for i in final:
		post.viewers.add(User.objects.get(email=i))
	send_push(final,data, email)

@login_required
def post(request, email, data):
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
		form = UserForm()
		return render(request, 'sign_up.html', {'form': form, 'type':'User'})

def signup_user_success(request):
	return HttpResponse('success')


def signup_rep(request):
	if request.method == 'POST':
		form = RepresentativeForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/signup/rep/success/')
		else:
			form = RepresentativeForm()
			return render(request, 'sign_up.html', {'form': form, 'type':'Representative'})
	else:
		form = RepresentativeForm()
		return render(request, 'sign_up.html', {'form': form, 'type':'Representative'})

def signup_rep_success(request):
	return HttpResponse('success')


def login(request):
	if request.method == 'POST':
		try:
			m = User.objects.get(email=request.POST['email'])
			if m.password == request.POST['password']:
				request.session['user_email'] = m.email
				return HttpResponseRedirect('/')
			else:
				form = LoginForm()
				form.errors['incorrect_pass'] = "Password Incorrect"
				return render(request,'login.html',{'form':form})
		except User.DoesNotExist:
			return HttpResponse("Your username and password didn't match.")
	else:
		if 'user_email' in request.session:
			return HttpResponse("You are already logged in")
		form = LoginForm()
		return render(request,'login.html',{'form':form})


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
    return render(request, "registration/register.html", {
        'form': form,
    })