from django.shortcuts import render,redirect,reverse
from Events.models import Events
from Amenities.models import Amenities

# Create your views here.

def home(request):
	amenities = Amenities.objects.all()
	events = Events.objects.all()

	return render(request,'index.html',{'amenities':amenities,'events':events})

def about_us(request):
	return render(request,'about-us.html')

def locate_us(request):
    return redirect(reverse('Home:about_us')+"#map")

def contact_us(request):
	return redirect(reverse('Inquiry:inquiry')+"#call_us")

def safety_measures(request):
	return render(request,'safety-measures.html')