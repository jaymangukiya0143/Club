from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
import random
from Amenities.models import Amenities

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext

def upload_img_path(instance, filename):
    new_filename = random.randint(1,1000)
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "events/{final_filename}".format(final_filename=final_filename)



class Events(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    amenity = models.ForeignKey(Amenities,on_delete=models.CASCADE,default=None)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    image1 = models.ImageField(upload_to=upload_img_path)
    smart1 = ImageSpecField(source='image1', processors=[ResizeToFill(500, 700)], format='JPEG')

    class Meta:
        permissions=(
            ('manage_events_and_tickets',"Can manage events and tickets"),
        )

    def __str__(self):
        return self.name

class Tickets(models.Model):
    event = models.ForeignKey(Events,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    collected = models.BooleanField(default=False)

    def __str__(self):
        return self.event.name + "-" + str(self.quantity)