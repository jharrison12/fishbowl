from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lottery.models import Bucket
from lottery.models import Slip
from lottery.forms import BucketForm
from lottery.forms import SlipForm
import random
from lottery.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def decode_url(str):
	return str.replace('_', ' ')

def encode_url(item):
	bob = str(item)
	bobb = bob.replace(' ', '_')
	return bobb


def index(request):
	context = RequestContext(request)
	#context_dict = {'boldmessage': "I'm a bold font from the context"}
	bucket_list = Bucket.objects.all()
	context_dict = {'buckets' : bucket_list}
	for bucket in bucket_list:
		bucket.url = bucket.name.replace(' ', '_') 
		bucket.url = bucket.url.replace("'", "")
		#return bucket.url
	return render_to_response('lottery/index.html', context_dict, context)



def bucket(request, bucket_name_url):
	context = RequestContext(request)
	bucket_name = bucket_name_url.replace('_', ' ')
	#bucket_name = bucket_name.replace("'", "-")
	context_dict = {'bucket_name': bucket_name}
	try:
		bucket = Bucket.objects.get(name=bucket_name)
		slips = list(Slip.objects.filter(Bucket=bucket))
		
		#papers = {i:v for i,v in enumerate(slips)}
		#context_dict['papers'] = papers	
		#context_dict['dictnum'] = dictnum	
		context_dict['slip'] = slips
		context_dict['bucket'] = bucket 
		context_dict['bucket_name_url'] = bucket_name_url
		#pull slip 
		if slips:
			"""def pull_slip(d):
				#bob = random.choice(d.values())
				bob = random.choice.pop(d.values())
				return encode_url(bob)
			"""
			slip_pulled1 = slips.pop(random.randrange(len(slips)))
			slip_pulled = encode_url(slip_pulled1)
			context_dict['slip_pulled'] = slip_pulled
			
		else:
			return render_to_response('lottery/bucket.html', context_dict, context)
	except Bucket.DoesNotExist:
		pass
	return render_to_response('lottery/bucket.html', context_dict, context)
	
def about(request):
	return HttpResponse("HI")
	
def add_bucket(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
		form = BucketForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
		
	else:
		form = BucketForm()
		
	return render_to_response('lottery/add_bucket.html', {'form':form}, context)
	
def add_slip(request, bucket_name_url):
	context = RequestContext(request)
	context_dict = {}
	bucket_list = Bucket.objects.all()
	bucket_name = decode_url(bucket_name_url)
	
	if request.method == 'POST':
		form = SlipForm(request.POST)
		if form.is_valid():
			slip = form.save(commit=False)
			try:
				buck = Bucket.objects.get(name=bucket_name)
				slip.bucket = buck
			except Bucket.DoesNotExist:
				return render_to_response('lottery/add_choice.html', {}, context)
			
			slip.save()
			
			return bucket(request, bucket_name_url)
		else:
			print form.errors
		
	else:
		form = SlipForm()
		
	context_dict['bucket_name_url'] = bucket_name_url
	context_dict['bucket_name'] = bucket_name
	context_dict['form'] = form
		
	return render_to_response('lottery/add_choice.html', context_dict, context)
	
def pull_slip(request, bucket_name_url, slip_pulled):
	context = RequestContext(request)
	bucket_name = decode_url(bucket_name_url)
	buckets = Bucket.objects.all()
	james = decode_url(slip_pulled)
	slips = Slip.objects.filter(Bucket=buckets)
	#delete the slip?
	Slip.objects.filter(name=james).delete()
	context_dict = {}
	context_dict['james'] = james
	context_dict['bucket_name_url'] = bucket_name_url
	context_dict['bucket_name'] = bucket_name
	
	return render_to_response('lottery/slip_pulled.html', context_dict, context)
	
def register(request):
	context = RequestContext(request)
	
	registered = False
	if request.method =='POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			#not sure about this?
			"""We also establish a link between the 
			two model instances that we create. After 
			creating a new User model instance, 
			we reference it in the UserProfile 
			instance with the line profile.user = user. 
			This is where we populate the user attribute of the 
			UserProfileForm form, which we hid from users in 
			Section 8.4.1."""
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	return render_to_response('lottery/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)
			
			
def user_login(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/lottery/')
			else:
				return HttpResponse("Your Fishbowl account is disabled")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login deteails supplied.")
	else:
		
		return render_to_response('lottery/login.html', {}, context)
		
@login_required		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/lottery/')