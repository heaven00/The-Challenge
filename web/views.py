# Create your views here.
from mongoengine.django.auth import User
from forms import UserCreationForm, AuthenticationForm, PostCreationForm, CommentForm
from django.shortcuts import render_to_response, RequestContext, redirect
from django.core.exceptions import ValidationError, PermissionDenied 
from document import Post
from django.views.decorators.http import require_http_methods
from functions import add_post, add_comment

"""Signup form using the basic django user creation form available"""

@require_http_methods(["GET","POST"])
def signup(request,**kwargs):
	context = {}
	if request.method == 'GET':
		form = UserCreationForm()
		context = {'form':form}
		return render_to_response('web/signup.html', RequestContext(request,context))
	elif request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print "data saved"
			context['message'] = 'Congratulations User Created'
			context['form'] = AuthenticationForm() 
			return  redirect('/user/login',permanent=True)
		else:
			context['form'] = form
			return render_to_response('web/signup.html', RequestContext(request,context))
			form = UserCreationForm()
		return render_to_response('web/signup.html', RequestContext(request,context))
	
@require_http_methods(["GET","POST"])
def login(request):
	context = {}
	if request.method == 'GET':
		form = AuthenticationForm()
		context['form'] = form
		return render_to_response('web/login.html', RequestContext(request,context))
	elif request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']	
			url = '/user/'+username+'/dashboard/'
			print url
			return redirect(url)
		else:
			context['form'] = form
			return render_to_response('web/login.html', RequestContext(request,context))
		return render_to_response('web/login.html', RequestContext(request,context))

@require_http_methods(["GET","POST"])	
def dashboard(request,**kwargs):
	context = {}
	if request.method == 'GET':
		user = kwargs['user']
		posts = Post.objects().order_by(user)
		context['posts'] = posts
		context['username'] = user
		context['form'] = CommentForm()
		return render_to_response('web/dashboard.html', RequestContext(request,context))
	elif request.method == 'POST':
		body = request.POST['body']
		user = kwargs['user']
		post_id = request.POST['comment']
		print post_id
		comments = add_comment(post_id,body,user)
		context['form'] = CommentForm()
		if comments:
			url = '/user/'+user+'/dashboard/'
			return redirect(url)
		else:
			return render_to_response('web/dashboard.html', RequestContext(request,context))
			
		
@require_http_methods(["GET","POST"])		
def post_handler(request,**kwargs):
	context = {}
	if request.method == 'GET':
		if 'post_id' in kwargs:
			instance = Post.objects(post_id=kwargs['post_id'])
			form = PostCreationForm(instance=instance)
		else:
			form = PostCreationForm()
		context['form'] = form
		return render_to_response('web/addpost.html', RequestContext(request,context))
	elif request.method == 'POST':
		if 'post_id' in kwargs:
			instance = Post.objects(post_id=kwargs['post_id'])
			form = PostCreationForm(request.POST,instance=instance)
		else:
			print request
			body = request.POST['body']
			user = kwargs['user']
			if "file" in request.FILES.items():
				print "Got File!!!"
				post = add_post(user,file,body)
			else:
				post = add_post(user,body)
			if post:
				url = '/user/'+user+'/dashboard/'
				return redirect(url)
			else:
				context['form'] = PostCreationForm()
				return render_to_response('web/addpost.html', RequestContext(request,context))
		return render_to_response('web/addpost.html', RequestContext(request,context))
