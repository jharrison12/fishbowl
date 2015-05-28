from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lottery.models import Bucket
from lottery.models import Slip
from lottery.forms import BucketForm
from lottery.forms import SlipForm
import random

def decode_url(str):
	return str.replace('_', ' ') and str.replace("'", "_")
	


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
		slips = Slip.objects.filter(Bucket=bucket)
		
		papers = {i:v for i,v in enumerate(slips)}
		context_dict['papers'] = papers	
		#context_dict['dictnum'] = dictnum	
		context_dict['slip'] = slips
		context_dict['bucket'] = bucket 
		context_dict['bucket_name_url'] = bucket_name_url
		#pull slip 
		if papers:
			def pull_slip(d):
				return random.choice(d.values())	
			slip_pulled = pull_slip(papers)
			context_dict['slip_pulled'] = slip_pulled
		else:
			pass 
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
				return render_to_response('lottery/add_choice.html', {'bucket_list': bucket_list}, context)
			
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
	slips = Slip.objects.filter(Bucket=buckets)
	
	
	context_dict = {}
	context_dict['slip_pulled'] = slip_pulled
	context_dict['bucket_name_url'] = bucket_name_url
	context_dict['bucket_name'] = bucket_name
	
	return render_to_response('lottery/slip_pulled.html', context_dict, context)
	
	