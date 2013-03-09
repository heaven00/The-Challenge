# Create your views here.
from mongoengine.django.auth import User
from forms import UserCreationForm
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import ValidationError, PermissionDenied 

"""Signup form using the basic django user creation form available"""

#!TODO TEMPLATES PENDING, Find Appropriate error to replace Permission Denied, 400 maybe

def signup(request,**kwargs):
	context = {}
	if request.method == 'GET':
		form = UserCreationForm()
		context = {'form':form}
		return render_to_response('web/signup.html',RequestContext(request,context))
	
	elif request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print "data saved"
			context['message'] = 'Congratulations User Created'
			return render_to_response('web/signup.html',RequestContext(request,context))
		else:
			context['form'] = form
			return render_to_response('web/signup.html',RequestContext(request,context))
			form = UserCreationForm()
		return render_to_response('web/signup.html',RequestContext(request,context))
	else:
		raise PermissionDenied('Invalid Request')
	

