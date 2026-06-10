from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    project_id = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Device(models.Model):
    device_id = models.CharField(max_length=255, primary_key=True)
    project = models.ForeignKey(Project,on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    console_port = models.IntegerField()
    device_type = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    
class Interface(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE, related_name='interfaces')
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    mask = models.GenericIPAddressField(null=True,blank=True)
    gateway = models.GenericIPAddressField(null=True,blank = True)
    is_configured = models.BooleanField(default= False)
    