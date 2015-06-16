from django.conf.urls import patterns, url
from lottery import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	#url(r'^about/', views.about, name='about'),
	#url(r'^bucket/', views.bucket, name='bucket'),
	url(r'^add_bucket/$', views.add_bucket, name='add_bucket'),
	#url(r'^add_choice/$', views.add_slip, name='add_slip'),
	url(r'^bucket/(?P<bucket_name_url>\w+)/$', views.bucket, name='bucket'),
	url(r'^bucket/(?P<bucket_name_url>\w+)/add_choice/$', views.add_slip, name='add_choice'),
	url(r'^bucket/(?P<bucket_name_url>\w+)/(?P<slip_pulled>\w+)/$', views.pull_slip, name='pull_slip'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	)