from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from .models import Payments
from Plans.models import Plans
from Amenities.models import Bookings
from Member.models import Member,Membership
from Events.models import Events,Tickets
from Amenities.models import Amenities

from datetime import *

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,login,logout
import random
import datetime

from django.core.mail import send_mail

# Create your views here.


def process_payment_plan(request,plan):
    if request.user.is_authenticated:
        user_obj = get_object_or_404(User, pk=request.user.id)
        member_obj = get_object_or_404(Member, member=user_obj.id)
        memberships = Membership.objects.filter(member=member_obj)
        eligible = True
        for m in memberships:
            if m.is_expired == False:
                eligible = False
                break

        if eligible:
            plan_obj = get_object_or_404(Plans,pk=plan)

            if len(Payments.objects.all()) > 0:
                ans = True
                while ans==True:
                    inv = str(plan_obj.id) + "-" + str(random.randint(11111,99999))
                    ans=False
                    for pay_obj in Payments.objects.all():
                        if pay_obj.invoice_id == inv:
                            ans=True
            else:
                inv = str(plan_obj.id) + "-" + str(random.randint(11111, 99999))


            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': plan_obj.fees,
                'item_name': plan_obj.name,
                'invoice': inv,
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format('localhost:3306',
                                                   reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format("localhost:3306",
                                                   reverse('Payments:payment_success_plan')),
                'cancel_return': 'http://{}{}'.format("localhost:3306",
                                                      reverse('Payments:payment_failed_plan')),
            }

            request.session['plan_id'] = plan_obj.id
            request.session['invoice_id'] = inv

            # payment = Payments()
            # payment.save()
            #
            # request.session['payment_id'] = payment.id

            form = PayPalPaymentsForm(initial=paypal_dict)

            return render(request, 'payment/process_payment_plan.html', {'form': form,'plan':plan_obj})
        else:
            return HttpResponse("<h3>You've already an active membership.</h3>")
    else:
        plan_obj = get_object_or_404(Plans, pk=plan)
        if len(Payments.objects.all()) > 0:
            ans = True
            while ans == True:
                inv = str(plan_obj.id) + "-" + str(random.randint(11111, 99999))
                ans = False
                for pay_obj in Payments.objects.all():
                    if pay_obj.invoice_id == inv:
                        ans = True
        else:
            inv = str(plan_obj.id) + "-" + str(random.randint(11111, 99999))

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': plan_obj.fees,
            'item_name': plan_obj.name,
            'invoice': inv,
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format('localhost:3306',
                                               reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format("localhost:3306",
                                               reverse('Payments:payment_success_plan')),
            'cancel_return': 'http://{}{}'.format("localhost:3306",
                                                  reverse('Payments:payment_failed_plan')),
        }

        request.session['plan_id'] = plan_obj.id
        request.session['invoice_id'] = inv

        # payment = Payments()
        # payment.save()
        #
        # request.session['payment_id'] = payment.id

        form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, 'payment/process_payment_plan.html', {'form': form, 'plan': plan_obj})


@csrf_exempt
def payment_success_plan(request):

    if request.user.is_authenticated:
        user_obj = get_object_or_404(User, pk=request.user.id)
        member_obj = get_object_or_404(Member, member=user_obj.id)

        plan_obj = get_object_or_404(Plans, id=request.session.get('plan_id'))

        membership = Membership()
        membership.member = member_obj
        membership.mem_plan = plan_obj
        membership.expiry_at = datetime.date.today() + datetime.timedelta(days=(plan_obj.duration * 30))
        membership.is_expired = False

        membership.save()

        payment_obj = Payments()
        payment_obj.status = True
        payment_obj.member = member_obj
        payment_obj.membership = membership

        payment_obj.amount = plan_obj.fees
        payment_obj.payment_for = "P"
        payment_obj.save()
        payment_obj.invoice_id = str(request.session.get('invoice_id')) + ":" + str(member_obj.id) + "_" + str(payment_obj.id)
        payment_obj.save()

        subject = "Thank you : You're now enrolled to new membership plan!"
        message = "\n\nDear " + request.user.first_name + " " + request.user.last_name + ",\n" + "Thank you for enrolling a membership plan again! We’re thrilled to have you on board and can’t wait to get to know you.\n\nYou can view our full calendar of events at http://localhost:3306/Club/view_events/.\n\nYou can view and book amenities at http://localhost:3306/Club/amenities/\n\nShould you need any assistance or have any questions or comments about your membership or benefits, please feel free to contact us at +918735983255 or email us at hawk4club@gmail.com or you can place query at http://localhost:3306/Club/inquiry/.\n\nWe look forward to seeing you at our next meeting!\n\nThank You!"
        email_from = settings.EMAIL_HOST_USER
        email_to = [request.user.email, ]
        send_mail(subject, message, email_from, email_to)


        return render(request, 'payment/payment_success_plan.html')
    else:
        member = request.session.get('member')
        plan_obj = get_object_or_404(Plans, id=request.session.get('plan_id'))
        print(member)
        user_obj = User.objects.create_user(member['email'], member['email'], member['password'])
        user_obj.first_name = member['Fname']
        user_obj.last_name = member['Lname']
        member_obj = Member()
        member_obj.member = user_obj
        member_obj.dob = member['dob']
        member_obj.address = member['address']
        member_obj.gender = member['gender']
        member_obj.phone = member['phone']
            # member_obj.occupation = member['occupation']
            # member_obj.no_fam_mem = member['no_fam_mem']
            # member_obj.image1 = member['image1']
            # member_obj.mem_plan = plan_obj
            # member_obj.is_active = False
            # member_obj.expiry_at = datetime.date.today() + datetime.timedelta(days=(plan_obj.duration * 30))

        user_obj.save()
        member_obj.save()

        membership = Membership()
        membership.member = member_obj
        membership.mem_plan = plan_obj
        membership.expiry_at = datetime.date.today() + datetime.timedelta(days=(plan_obj.duration * 30))
        membership.is_expired = False


        membership.save()

            # login(request,user_obj)

        payment_obj = Payments()
        # payment_id = request.session.get('payment_id')
        payment_obj.status = True
        payment_obj.member = member_obj
        payment_obj.membership = membership

        payment_obj.amount = plan_obj.fees
        payment_obj.payment_for = "P"
        payment_obj.save()
        payment_obj.invoice_id = str(request.session.get('invoice_id')) + ":" + str(member_obj.id) + "_" + str(payment_obj.id)
        payment_obj.save()

        member_obj = get_object_or_404(Member,id=payment_obj.member.id)
        member_obj.is_active = True
        member_obj.save()
        login(request,user_obj)

        subject = "Thank you : You're our Member Now!"
        message = "\n\nDear " + request.user.first_name + " " + request.user.last_name + ",\n" + "Thank you so much for becoming a member of Hawk Club! We’re thrilled to have you on board and can’t wait to get to know you.\n\nYou can view our full calendar of events at http://localhost:3306/Club/view_events/.\n\nYou can view and book amenities at http://localhost:3306/Club/amenities/\n\nShould you need any assistance or have any questions or comments about your membership or benefits, please feel free to contact us at +918735983255 or email us at hawk4club@gmail.com or you can place query at http://localhost:3306/Club/inquiry/.\n\nWe look forward to seeing you at our next meeting!\n\nThank You!"
        email_from = settings.EMAIL_HOST_USER
        email_to = [request.user.email, ]
        send_mail(subject, message, email_from, email_to)

        return render(request,'payment/payment_success_plan.html')

@csrf_exempt
def payment_failed_plan(request):
    request.session.delete()
    return render(request,'payment/payment_failed_plan.html')








def process_payment_ticket(request,event):

    event_obj = get_object_or_404(Events,pk=event)

    if len(Payments.objects.all()) > 0:
        ans = True
        while ans==True:
            inv = str(event_obj.id) + "-" + str(random.randint(11111,99999))
            ans=False
            for pay_obj in Payments.objects.all():
                if pay_obj.invoice_id == inv:
                    ans=True
    else:
        inv = str(event_obj.id) + "-" + str(random.randint(11111, 99999))

    quantity = request.POST['quantity']
    total = float(quantity) * float(event_obj.price)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': event_obj.name,
        'invoice': inv,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format('localhost:3306',
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("localhost:3306",
                                           reverse('Payments:payment_success_ticket')),
        'cancel_return': 'http://{}{}'.format("localhost:3306",
                                              reverse('Payments:payment_failed_plan')),
    }

    request.session['event_id'] = event_obj.id
    request.session['invoice_id'] = inv
    request.session['quantity'] = quantity
    request.session['total'] = total

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'payment/process_payment_ticket.html', {'form': form,'event':event_obj})


@csrf_exempt
def payment_success_ticket(request):

    event_id = request.session.get('event_id')
    inv = request.session.get('invoice_id')

    event_obj = get_object_or_404(Events,pk=event_id)
    event_obj.capacity -= request.session.get('quantity')
    event_obj.save()

    tickets = Tickets(event=event_obj,quantity=request.session.get('quantity'))
    tickets.save()

    member_obj = get_object_or_404(Member,member=request.user)

    payment_obj = Payments(member=member_obj,ticket=tickets,amount=request.session.get('total'),status=True,payment_for = "E")
    payment_obj.save()

    payment_obj.invoice_id = str(request.session.get('invoice_id')) + ":" + str(member_obj.id) + "_" + str(payment_obj.id)
    payment_obj.save()

    subject = "Tickets Booked!"
    message = "\n\nHi " + request.user.first_name + " " + request.user.last_name + ",\n" + "Your tickets has been booked successfully!\n\nWe are sending this mail to let you know that you have a confirmed booking of tickets of " + event_obj.name + " with us.\n\n\nCheers! and see you at Club.\n\nInstruction:\nShow the Ticket Id at the Club office to collect your physical Tickets.\n\nYour Ticket Id is " + payment_obj.invoice_id + "  (Don't share it with anyone!)"
    email_from = settings.EMAIL_HOST_USER
    email_to = [request.user.email, ]
    send_mail(subject, message, email_from, email_to)

    return render(request,'payment/payment_success_ticket.html')

@csrf_exempt
def payment_failed_plan(request):
    request.session.delete()
    return render(request, 'payment/payment_failed_plan.html')









def process_payment_booking(request,booking):

    booking_obj = get_object_or_404(Bookings,pk=booking)

    if len(Payments.objects.all()) > 0:
        ans = True
        while ans == True:
            inv = str(booking_obj.amenity.id) + "-" + str(random.randint(11111, 99999))
            ans = False
            for pay_obj in Payments.objects.all():
                if pay_obj.invoice_id == inv:
                    ans = True
    else:
        inv = str(amenity_obj.id) + "-" + str(random.randint(11111, 99999))

    paypal_dict = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : booking_obj.total,
        'item_name' : booking_obj.amenity.name,
        'invoice' : inv,
        'currency_code' : 'USD',
        'notify_url' : 'http://{}{}'.format('localhost:3306',reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("localhost:3306",
                                           reverse('Payments:payment_success_booking')),
        'cancel_url' : 'http://{}{}'.format('localhost:3306',reverse('Payments:payment_failed_plan'))
    }

    amenity_obj = get_object_or_404(Amenities,pk=booking_obj.amenity.id)

    request.session['booking_id'] = booking_obj.id
    request.session['invoice_id'] = inv

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request,'payment/process_payment_booking.html',{'form':form,'amenity':amenity_obj,'booking':booking_obj})

@csrf_exempt
def payment_success_booking(request):

    booking_id = request.session.get('booking_id')
    booking_obj = get_object_or_404(Bookings,pk=booking_id)
    total = request.session.get('total')
    invoice = request.session.get('invoice_id')

    member_obj = get_object_or_404(Member,member=request.user)

    booking_obj.confirm = True
    booking_obj.save()

    payment = Payments(booking=booking_obj,member=member_obj,invoice_id=invoice,status=True,amount=booking_obj.total,payment_for="B")
    payment.save()

    invoice = request.session.get('invoice_id')+":" + str(member_obj.id) + "_" + str(payment.id)
    payment.invoice_id = invoice
    payment.save()

    return render(request,'payment/payment_success_booking.html')