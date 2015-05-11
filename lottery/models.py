from django.db import models

# Create your models here.
class Bucket(models.Model):
	name = models.CharField(max_length=128, unique=True)
	
	def __unicode__(self):
		return self.name 
		
class Slip(models.Model):
	Bucket = models.ForeignKey(Bucket)
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name