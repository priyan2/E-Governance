from django.conf import settings
from django.db import models
from django.utils import timezone


class Public_Detail(models.Model):
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    image = models.FileField('Upload Image',upload_to='documents/',null=True)
    status=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.username
class Category_Detail(models.Model): 
    category_name = models.CharField(max_length=30)
    def __str__(self):
        return self.category_name
class Rise_Complaint(models.Model):
	reference_id = models.IntegerField(primary_key=True)
	public_id = models.ForeignKey(Public_Detail, on_delete=models.CASCADE,null=True)
	area = models.CharField(max_length=300)
	address = models.TextField(max_length=2000)
	service_id = models.ForeignKey(Category_Detail, on_delete=models.CASCADE,null=True,blank=True)
	msg = models.TextField(max_length=2000)
	date = models.DateField(default=timezone.now(),null=True)
	video = models.FileField('Upload Image/Video',upload_to='video/',null=True)
	status= models.CharField(max_length=300)
	initial_status = models.CharField(max_length=300)

	def publish(self):
		self.date = timezone.now()
		self.save()
	def __str__(self):
		return self.area
class Feedback(models.Model):
	name= models.CharField(max_length=300,null=True)
	email= models.CharField(max_length=300,null=True)
	mobile= models.CharField(max_length=300,null=True)
	comment = models.TextField(max_length=1000,null=True)
	date = models.DateField('Posted Date',default=timezone.now())
	def __str__(self):
		return self.name
	def publish(self):
		self.date = timezone.now()
		self.save()

class Staff_Detail(models.Model):
    staffid = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username
