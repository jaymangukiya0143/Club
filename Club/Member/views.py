from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from .models import Member,Membership
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from random import randint
from django.core.mail import send_mail
from Club import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

from Amenities.models import Bookings,Amenities
from Plans.models import Plans

from datetime import *
from Payments.models import Payments
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('Home:home')
    else:
        if request.method == 'POST':
            Fname = request.POST['Fname'].capitalize()
            Lname = request.POST['Lname'].capitalize()
            email = request.POST['email'].lower()
            password1 = request.POST['password']
            password2 = request.POST['password2']

            members = Member.objects.all()
            flag = True
            for m in members:
                if m.member.email == email:
                    flag = False
                    break

            if flag == True:
                if password1 == password2:
                    gender = request.POST['gender']
                    phone = request.POST['phone']
                    dob = request.POST['dob']
                    # occupation = request.POST['occupation']
                    # no_fam_mem = request.POST['no_fam_mem']

                    if (request.POST['addressline2'] != ""):
                        add = request.POST['addressline1'] + ", " + request.POST['addressline2'] + ", " + request.POST['city'] + ", " + request.POST['state'] + " - " + request.POST['postal']
                    else:
                        add = request.POST['addressline1'] + ", " + request.POST['city'] + ", " + request.POST['state'] + " - " + request.POST['postal']

                    address = add
                    # if request.FILES:
                    #     image1 = request.FILES['image1']
                    # else:
                    #     image1 = " "


                    # member = {'Fname':Fname,'Lname':Lname,'email':email,'password':password1,'address':address,'dob':dob,'gender':gender,'occupation':occupation,'phone':phone,'no_fam_mem':no_fam_mem}
                    member = {'Fname': Fname, 'Lname': Lname, 'email': email, 'password': password1, 'address': address,'phone':phone,
                              'dob': dob, 'gender': gender}

                    otp = randint(111111,999999)
                    subject = "OTP from Hawk Club"
                    message = "Your otp for email verification is " + str(otp)
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [email,]
                    send_mail(subject,message,email_from,email_to)
                    request.session['email_verification_otp'] = str(otp)
                    request.session['member'] = member

                    return redirect('Member:email_otp_verification')
                else:
                    pass
            else:
                pass

        return render(request,'member/signup.html')

def check_eligiblity(member_obj):
    memberships = Membership.objects.filter(member=member_obj)
    eligible = False
    for m in memberships:
        if m.is_expired == False:
            eligible = True
            break

    return eligible

def login_member(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        pwd = request.POST['password']
        usr = authenticate(request,username=email,password=pwd)

        if usr:
            usr = User.objects.get(username=email)
            usr_name = usr.first_name + " " + usr.last_name
            if usr.is_active == True:
                member_obj = get_object_or_404(Member, member=usr)
                memberships = Membership.objects.filter(member=member_obj)

                for m in memberships:
                    if datetime.today().date() > m.expiry_at:
                        m.is_expired = True

                eligible = check_eligiblity(member_obj)

                if eligible:
                    login(request, usr)
                    return redirect('Home:home')
                else:
                    login(request, usr)
                    memberships = Membership.objects.filter(member__member=request.user.id)
                    return render(request,'member/renew_plan/renew_plan.html',{'membership':memberships})
            else:
                return HttpResponse("Your account is deactivated")
    else:
        if request.user.is_authenticated:
            user = get_object_or_404(User,id=request.user.id)
            member_obj = get_object_or_404(Member,member=user)

            eligible = check_eligiblity(member_obj)

            if eligible:
                return redirect('Home:home')
            else:
                memberships = Membership.objects.filter(member__member=request.user.id)
                return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})
        else:
            return render(request,'member/login.html')

def logout_member(request):
    request.session.delete()
    logout(request)
    return redirect('Home:home')

def otp_sent(request):
    pass

def email_otp_verification(request):
    if request.method == 'POST':
        otp2 = request.POST['otp']
        otp1 = request.session.get('email_verification_otp')
        print(otp2)
        print(otp1)
        if otp1 == otp2:
            return redirect('Plans:view_plans')
    return render(request,'member/otp_verification.html')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            old_pwd = request.POST['old_password']
            new_pwd = request.POST['new_password']
            new_pwd2 = request.POST['new_password2']
            user_obj = User.objects.get(email=request.user.email)

            email = request.user.email

            if (user_obj.check_password(old_pwd)) and (new_pwd == new_pwd2):
                user_obj.set_password(new_pwd)
                user_obj.save()

                subject = "Password changed successfully!"
                message = "Hi, " + user_obj.first_name + " " + user_obj.last_name + ",\n\nThis mail is to inform you that you have successfully changed password."
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)

                return redirect('Home:home')
        return render(request,'member/change_password.html')
    else:
        return redirect('Member:login_member')

def forgot_password(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email'].lower()
            request.session['reset_email'] = email

            otp = randint(111111, 999999)
            subject = "Reset Password OTP from Hawk Club"
            message = "Your otp for reset password is " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)
            request.session['reset_password_otp'] = str(otp)

            return redirect('Member:reset_otp')
        return render(request,'member/forgot_password.html')
    else:
        return redirect('Home:home')

def reset_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        new_pwd = request.POST['password1']
        new_pwd2 = request.POST['password2']
        sent_otp = request.session.get('reset_password_otp')
        email = request.session.get('reset_email')

        if (otp == sent_otp) and (new_pwd == new_pwd2):
            member = User.objects.get(email=request.session.get('reset_email'))
            member.set_password(new_pwd)
            member.save()

            subject = "Password changed successfully!"
            message = "Hi, " + member.first_name + " " + member.last_name + ",\n\nThis mail is to inform you that you have successfully changed password."
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)

            return redirect('Member:login_member')
    return render(request,'member/reset_otp.html')


def profile(request):
    if request.user:
        member_obj = get_object_or_404(Member,member=request.user)
        return render(request,'member/profile.html',{'member':member_obj})

def edit_profile(request):
    if request.method == 'POST':
        Fname = request.POST['Fname'].capitalize()
        Lname = request.POST['Lname'].capitalize()
        phone = request.POST['phone']
        address = request.POST['address']
        dob = request.POST['dob']
        gender = request.POST['gender']
        # occupation = request.POST['occupation']
        # no_fam_mem = request.POST['no_fam_mem']

        member_obj = get_object_or_404(Member, member=request.user)

        if 'image1' in request.FILES:
            image1 = request.FILES['image1']
        else:
            image1 = member_obj.image1


        member_obj.member.first_name = Fname
        member_obj.member.last_name = Lname
        member_obj.phone = phone
        member_obj.address = address
        member_obj.dob = dob
        member_obj.gender = gender
        # member_obj.occupation = occupation
        # member_obj.no_fam_mem = no_fam_mem
        member_obj.image1 = image1
        member_obj.save()
        user_obj = get_object_or_404(User,username=request.user.email)
        user_obj.first_name = Fname
        user_obj.last_name = Lname
        user_obj.save()
        return redirect('Member:profile')
    else:
        member_obj = get_object_or_404(Member, member=request.user)
        dob = str(member_obj.dob)
        return render(request,'member/edit_profile.html',{'member':member_obj,'dob':dob})




def my_bookings(request):
    user = get_object_or_404(User,email=request.user)
    member = get_object_or_404(Member,member=user.id)
    member_id = member.id
    bookings = Bookings.objects.filter(member=member_id)
    no_of_bookings = len(bookings)

    return render(request,'member/bookings/my_bookings.html',{'bookings':bookings,'no_of_bookings':no_of_bookings})

def view_booking(request,booking):
    booking = get_object_or_404(Bookings,pk=booking)
    payment = get_object_or_404(Payments, booking=booking)
    return render(request,'member/bookings/view_booking.html',{'booking':booking,'payment':payment})


def my_tickets(request):
    user = get_object_or_404(User, email=request.user)
    member = get_object_or_404(Member, member=user.id)
    member_id = member.id
    payments = Payments.objects.filter(payment_for="E",member=member_id)
    no_of_payments = len(payments)
    return render(request,'member/tickets/my_tickets.html',{'tickets':payments,'no_of_tickets':no_of_payments})

def view_ticket(request,payment):
    payment = get_object_or_404(Payments,pk=payment)
    return render(request,'member/tickets/view_ticket.html',{'ticket':payment})


def my_payments(request):
    user = get_object_or_404(User, email=request.user)
    member = get_object_or_404(Member, member=user.id)
    member_id = member.id
    payments = Payments.objects.filter(member=member_id)
    plan_payment = len(Payments.objects.filter(member=member_id,payment_for='P'))
    booking_payment = len(Payments.objects.filter(member=member_id, payment_for='B'))
    ticket_payment = len(Payments.objects.filter(member=member_id, payment_for='E'))
    no_of_payments = len(payments)
    return render(request,'member/payments/my_payments.html',{'payments':payments,'no_of_payments':no_of_payments,'plan_payment':plan_payment,'booking_payment':booking_payment,'ticket_payment':ticket_payment})

def my_plans(request):
    user = get_object_or_404(User, email=request.user)
    member = get_object_or_404(Member, member=user.id)
    membership = Membership.objects.filter(member=member.id)
    membership = sorted(membership,key=lambda m:m.brought_at, reverse=True)
    return render(request,'member/renew_plan/my_plans.html',{'membership':membership})

def view_plan(request,pk):
    membership = get_object_or_404(Membership,pk=pk)
    payment = get_object_or_404(Payments,membership=membership.id)
    return render(request,'member/renew_plan/view_plan.html',{'membership':membership,'payment':payment})

def view_payment(request,payment):
    payment = get_object_or_404(Payments,pk=payment)
    return render(request,'member/payments/view_payment.html',{'payment':payment})

@csrf_exempt
def validate_email(request):
    email = request.POST['email'].lower()
    password = request.POST['password']
    email_exists = User.objects.filter(username__iexact=email,is_staff=False).exists()
    password_matches = authenticate(username=email,password=password)

    if email_exists:
        if password_matches:
            data = {
                'is_exists' : 'True',
                'password_matches': 'True'
            }
        else:
            data = {
                'is_exists':'True',
                'password_matches':'False'
            }
    else:
        data={
            'is_exists':'False'
        }

    return JsonResponse(data)

@csrf_exempt
def validate_email_signup(request):
    email = request.POST['email'].lower()

    email_exists = User.objects.filter(username__iexact=email,is_staff=False).exists()

    if email_exists:
        data = {
            'is_exists' : 'True',
        }
    else:
        data = {
            'is_exists':'False',
        }
    return JsonResponse(data)


@csrf_exempt
def validate_otp(request,req_from):

    if req_from == 1:
        sent_otp = request.session.get('email_verification_otp')
    elif req_from == 2:
        sent_otp = request.session.get('reset_password_otp')
    entered_otp = request.POST['otp']

    if str(sent_otp) == str(entered_otp):
        data={
            'is_same':'True'
        }
    else:
        data = {
            'is_same': 'False'
        }
    return JsonResponse(data)

@csrf_exempt
def validate_password(request):
    email = request.user.email
    password = request.POST['old_password']
    password_matches = authenticate(username=email, password=password)

    if password_matches:
        data={
            'is_matches':'True'
        }
    else:
        data={
            'is_matches':'False'
        }
    print(data)
    return JsonResponse(data)


def send_booking_request(request,pk):
    user = get_object_or_404(User, id=request.user.id)
    member_obj = get_object_or_404(Member, member=user)
    memberships = Membership.objects.filter(member=member_obj)

    eligible = check_eligiblity(member_obj)

    if eligible:
        amenity_obj = get_object_or_404(Amenities, pk=pk)
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        no_of_slots = request.POST['no_of_slots']
        total = request.POST['total']

        member_obj = get_object_or_404(Member, member=request.user)

        booking = Bookings(amenity=amenity_obj, member=member_obj, from_date=from_date, to_date=to_date, to_time=to_time,
                           from_time=from_time, no_of_slots=no_of_slots, total=total, status=False, confirm=False)
        booking.save()

        return redirect('Member:booking_request')
    else:
        memberships = Membership.objects.filter(member__member=request.user.id)
        return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})


def booking_request(request):
    user = get_object_or_404(User, id=request.user.id)
    member_obj = get_object_or_404(Member, member=user)
    memberships = Membership.objects.filter(member=member_obj)

    eligible = check_eligiblity(member_obj)

    if eligible:
        bookings_obj = Bookings.objects.filter(confirm=False,member__member__username=request.user)
        return render(request, 'amenities/booking_requests.html', {'bookings': bookings_obj})
    else:
        memberships = Membership.objects.filter(member__member=request.user.id)
        return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})