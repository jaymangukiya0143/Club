from django.urls import path
from . import views

app_name = 'Feedback'

urlpatterns=[
    path('give_feedback/',views.give_feedback,name='give_feedback'),
]