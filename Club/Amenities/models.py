from django.db import models
from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
import os
import random

from Member.models import Member


# Create your models here.

Amenity_Type = (('A1','Amenity'),('A2','Activity'))
TIME = (('M','Morning'),('E','Evening'))

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext

def upload_img_path(instance, filename):
    new_filename = random.randint(1,1000)
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "amenities/{final_filename}".format(final_filename=final_filename)

class Amenities(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    occupancy = models.PositiveIntegerField()
    amenity_type = models.CharField(choices=Amenity_Type,default='',max_length=8)
    rate = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    image1 = models.ImageField(upload_to=upload_img_path)
    image2 = models.ImageField(upload_to=upload_img_path)
    image3 = models.ImageField(upload_to=upload_img_path)
    image4 = models.ImageField(upload_to=upload_img_path)
    smart1 = ImageSpecField(source='image1', processors=[ResizeToFill(500, 700)], format='JPEG')
    smart2 = ImageSpecField(source='image2', processors=[ResizeToFill(500, 700)], format='JPEG')
    smart3 = ImageSpecField(source='image3', processors=[ResizeToFill(500, 700)], format='JPEG')
    smart4 = ImageSpecField(source='image4', processors=[ResizeToFill(500, 700)], format='JPEG')

    def __str__(self):
        return self.name


class Bookings(models.Model):
    amenity = models.ForeignKey(Amenities,on_delete=models.CASCADE)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    from_date = models.DateField(null=False,blank=False)
    from_time = models.CharField(choices=TIME,default='',max_length=1)
    to_date = models.DateField(null=False,blank=False)
    to_time = models.CharField(choices=TIME, default='', max_length=1)
    no_of_slots = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    total = models.CharField(max_length=7)
    status = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)

    class Meta:
        permissions=(
            ("view_booking","Can view all the bookings"),
        )

    def __str__(self):
        return self.amenity.name