from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Feedback(models.Model):
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback = models.TextField(default='')
    given_at = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=45)

    def __str__(self):
        return self.member.username