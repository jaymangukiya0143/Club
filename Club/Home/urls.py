from django.urls import path
from . import views

app_name = 'Home'

urlpatterns = [
    path('home/',views.home,name='home'),
    path('about_us/',views.about_us,name='about_us'),
    path('locate_us/',views.locate_us,name='locate_us'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('safety_measures/', views.safety_measures, name='safety_measures'),
]