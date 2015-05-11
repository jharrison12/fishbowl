from django import forms
from lottery.models import Bucket
from lottery.models import Slip


class BucketForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="I NEED A NAME")
	
	class Meta:
		model = Bucket
		#fields = ('name')

		
class SlipForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please add a choice you would like to win later")
	
	class Meta:
		model = Slip
		#fields = ('name')