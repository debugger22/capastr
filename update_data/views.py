from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from datalink.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def name(request):
	if request.method == 'POST':
		user = User.objects.get(mainuser=request.user)
		#try:
		temp = request.POST.get('new_name').split(" ")
		user.first_name = temp[0]
		user.last_name = temp[1]
		user.save()
		return HttpResponseRedirect('/accounts/profile/')
		#except:
			#return HttpResponse('something bad happened')
	else:
		return HttpResponse('no data submitted')

@login_required
def email(request):
	if request.method == 'POST':
		user = User.objects.get(mainuser=request.user)
		try:
			user.email = request.POST.get('new_email')
			user.save()
			return HttpResponseRedirect('/accounts/profile/')
		except:
			return HttpResponse('something bad happened')
	else:
		return HttpResponse('no data submitted')

@login_required
def mobile(request):
	if request.method == 'POST':
		user = User.objects.get(mainuser=request.user)
		try:
			user.mobile = request.POST.get('new_mobile')
			user.save()
			return HttpResponseRedirect('/accounts/profile/')
		except:
			return HttpResponse('something bad happened')
	else:
		return HttpResponse('no data submitted')

@login_required
def tags(request):
	if request.method == 'POST':
		user = User.objects.get(mainuser=request.user)
		try:
			temp = request.POST.get('new_tags').split(",")
			user.tags.clear()
			for i in temp:
				user.tags.add(i.strip(" "))
			user.save()
			return HttpResponseRedirect('/accounts/profile/')
		except:
			return HttpResponse('something bad happened')
	else:
		return HttpResponse('no data submitted')
