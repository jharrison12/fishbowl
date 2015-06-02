from django import forms
from lottery.models import Bucket
from lottery.models import Slip
from lottery.models import UserProfile
from django.contrib.auth.models import User



class BucketForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="I NEED A NAME")
	
	class Meta:
		model = Bucket
		#fields = ('name')

		
class SlipForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please add a choice you would like to win later")
	
	class Meta:
		model = Slip
		#fields = ('title')
		
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserProfile
		#fields = ('picture')