from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
import random
from Club import settings
from datetime import datetime,timedelta
from Plans.models import Plans

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext

def upload_member_image_path(instance, filename):
    new_filename = random.randint(1,1000)
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "members/{final_filename}".format(final_filename=final_filename)

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female')
)

class Member(models.Model):
    member = models.OneToOneField(User,on_delete=models.CASCADE)
    dob = models.DateField(null=False,blank=False)
    address = models.TextField(null=False,blank=False)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    phone = models.CharField(max_length=10,null=False,blank=False)
    # occupation = models.CharField(max_length=20)
    # no_fam_mem = models.IntegerField()
    image1 = models.ImageField(upload_to=upload_member_image_path,null=True,blank=True,default=" ")
    smart1 = ImageSpecField(source='image1', processors=[ResizeToFill(250, 350)], format='JPEG')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.username


class Membership(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    mem_plan = models.ForeignKey(Plans,on_delete=models.CASCADE)
    is_expired = models.BooleanField(default=False)
    expiry_at = models.DateField(null=False, blank=False)
    brought_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.member.first_name + " " + self.member.member.last_name