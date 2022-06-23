from django.db import models


# Create your models here.

class Inquiry(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=12)
    subject = models.CharField(max_length=30)
    message = models.TextField(default='')
    reply = models.TextField(default='',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    replied_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions=(
            ('manage_inquiries_and_feedbacks','Can manage inquiries and feedbacks'),
        )

    def __self__(self):
        return self.name

