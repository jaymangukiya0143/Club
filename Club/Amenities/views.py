from django.shortcuts import render,redirect,get_object_or_404,reverse
from .forms import AmenitiesForm,BookingForm
from .models import Amenities,Bookings
from Member.views import check_eligiblity
# from Club.Payments import models
from django.contrib.auth.models import User

from Member.models import Member,Membership

def add_amenity(request):
    if request.method == 'POST':
        amenity_form = AmenitiesForm(request.POST or None, request.FILES or None)
        if amenity_form.is_valid():
            amenity_form.save()
            print(amenity_form)
            return redirect('Amenities:amenities')
    else:
        amenity_form = AmenitiesForm()
    return render(request,'amenities/add_amenity.html',{'amenity_form':amenity_form})

def amenities(request):
    amenities = Amenities.objects.all()
    return render(request,'amenities/amenities.html',{'amenities':amenities})

def activities(request):
    amenities = Amenities.objects.all()
    return redirect(reverse('Amenities:amenities')+'#activities')

def single_amenity(request,pk):
    amenity = get_object_or_404(Amenities,pk=pk)
    return render(request,'amenities/single_amenity.html',{'amenity':amenity})

def book_amenity(request,pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        member_obj = get_object_or_404(Member, member=user)

        eligible = check_eligiblity(member_obj)

        if eligible:
            amenity = get_object_or_404(Amenities,pk=pk)
            return render(request, 'amenities/book_amenity.html',{'amenity':amenity})
        else:
            memberships = Membership.objects.filter(member__member=request.user.id)
            return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})
    else:
        return redirect('Member:login_member')