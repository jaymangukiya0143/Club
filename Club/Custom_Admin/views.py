from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate,login,logout
from Plans.models import Plans
from Plans.forms import PlanForm
from Amenities.models import Amenities,Bookings
from Amenities.forms import AmenitiesForm
from Events.models import Events,Tickets
from Events.forms import EventForm
from Inquiry.models import Inquiry
from Inquiry.forms import InquiryForm
from Feedback.models import Feedback
from Payments.models import Payments
from Member.models import Member,Membership

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from Club import settings
from django.contrib import messages
from django.core.mail import send_mail

from random import randint

#for pdf
from io import StringIO,BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


from django.views.generic import View,TemplateView


from django.http import HttpResponseRedirect

# Create your views here.



def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request,'custom_admin/dashboard.html')
    else:
        return redirect('Custom_Admin:admin_login')


def admin_login(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('Custom_Admin:dashboard')
    else:
        if request.method == 'POST':
            user = request.POST['username'].lower()
            pwd = request.POST['password']
            usr = authenticate(request,username=user,password=pwd)

            if usr:
                usr = User.objects.get(username=user)
                if usr.is_superuser == True or usr.is_staff == True:
                    login(request,usr)
                    admin = {'name':usr.username,'email':usr.email}
                    request.session['admin'] = admin
                    request.session['admin_email'] = usr.email
                    return redirect('Custom_Admin:dashboard')
                else:
                    return redirect('Member:login_member')
        return render(request,'custom_admin/account/login.html')


def admin_logout(request):
    # if request.session.get('admin'):
    request.session.delete()
    logout(request)
    return redirect('Custom_Admin:admin_login')


def admin_forgot_password(request):
    if not request.user.is_superuser or not request.user.is_staff:
        if request.method == 'POST':
            username = request.POST['username'].lower()

            admin_obj = get_object_or_404(User,username=username,is_superuser=True)
            request.session['admin_email'] = admin_obj.email

            otp = randint(111111,999999)
            request.session['reset_otp'] = otp

            subject = "Reset Password OTP from Hawk Club"
            message = "Your otp for reset password is " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            email_to = [admin_obj.email, ]
            send_mail(subject, message, email_from, email_to)

            return render(request,'Custom_Admin/account/reset_password.html')
        else:
            return render(request,'custom_admin/account/forgot_password.html')
    else:
        pass

def admin_reset_password(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        sent_otp = request.session.get('reset_otp')
        admin_email = request.session.get('admin_email')

        if (otp == sent_otp or password1 == password2):
            # print("in in in in")
            admin = User.objects.get(email=request.session.get('admin_email'))
            admin.set_password(password1)
            admin.save()

            subject = "Password changed successfully!"
            message = "Hi, " + admin.first_name + " " + admin.last_name + ",\n\nThis mail is to inform you that you have successfully changed password."
            email_from = settings.EMAIL_HOST_USER
            email_to = [admin_email, ]
            send_mail(subject, message, email_from, email_to)

            return redirect('Custom_Admin:admin_login')
        else:
            return render(request,'Custom_Admin/account/reset_password.html')
    else:
        return render(request,'Custom_Admin/account/reset_password.html')

def admin_change_password(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            old_pwd = request.POST['old_password']
            new_pwd = request.POST['new_password']
            new_pwd2 = request.POST['new_password2']

            admin_obj = User.objects.get(email=request.session.get('admin_email'))
            email = request.session.get('admin_email')

            if (admin_obj.check_password(old_pwd)) and (new_pwd == new_pwd2):
                admin_obj.set_password(new_pwd)
                admin_obj.save()

                subject = "Password changed successfully!"
                message = "Hi, " + admin_obj.first_name + " " + admin_obj.last_name + ",\n\nThis mail is to inform you that you have successfully changed password."
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)

                return redirect('Custom_Admin:profile')
            else:
                pass
        else:
            return render(request,'custom_admin/account/change_password.html')
    else:
        return redirect('Custom_Admin:admin_login')

def profile(request):
    if request.user.is_superuser or request.user.is_staff:
        admin = request.user
        return render(request,'custom_admin/account/profile.html',{'admin':admin})
    else:
        return redirect('Custom_Admin:admin_login')

def all_plans(request):
    if request.user.is_superuser or request.user.is_staff:
        plans = Plans.objects.all()
        return render(request,'custom_admin/plans/all_plans.html',{'plans':plans})
    else:
        return redirect('Custom_Admin:admin_login')

def add_plan(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            plan_form = PlanForm(request.POST or None)
            if plan_form.is_valid():
                plan_form.save()
                return redirect('Custom_Admin:all_plans')
            else:
                pass
        else:
            plan_form = PlanForm()
        return render(request,'custom_admin/plans/add_plan.html',{'plan_form':plan_form})
    else:
        return redirect('Custom_Admin:admin_login')

def view_plan(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        plan = get_object_or_404(Plans,pk=pk)
        return render(request,'custom_admin/plans/view_plan.html',{'plan':plan})
    else:
        return redirect('Custom_Admin:admin_login')

def edit_plan(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            plan_obj = get_object_or_404(Plans,pk=pk)
            plan_obj.name = request.POST['name']
            plan_obj.description = request.POST['description']
            plan_obj.duration = request.POST['duration']
            plan_obj.fees = request.POST['fees']
            plan_obj.save()
            return redirect('Custom_Admin:all_plans')
        else:
            plan = get_object_or_404(Plans,pk=pk)
            return render(request,'custom_admin/plans/edit_plan.html',{'plan':plan})
    else:
        return redirect('Custom_Admin:admin_login')

def delete_plan(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        plan_obj = get_object_or_404(Plans,pk=pk)
        plan_obj.delete()
        return redirect('Custom_Admin:all_plans')
    else:
        return redirect('Custom_Admin:admin_login')





def all_amenities(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            amenities = Amenities.objects.all()
            return render(request,'custom_admin/amenities/all_amenities.html',{'amenities':amenities})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')


def add_amenity(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            if request.method == 'POST':
                amenity_form = AmenitiesForm(request.POST or None, request.FILES or None)
                if amenity_form.is_valid():
                    amenity_form.save()
                    return redirect('Custom_Admin:all_amenities')
            else:
                amenity_form = AmenitiesForm()
            return render(request,'custom_admin/amenities/add_amenity.html',{'amenity_form':amenity_form})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def view_amenity(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            amenity = get_object_or_404(Amenities,pk=pk)
            return render(request,'custom_admin/amenities/view_amenity.html',{'amenity':amenity})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def edit_amenity(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            if request.method == 'POST':
                amenity_obj = AmenitiesForm(request.POST or None, request.FILES or None, instance=get_object_or_404(Amenities,pk=pk))
                if amenity_obj.is_valid():
                    amenity_obj.save()
                    return redirect('Custom_Admin:all_amenities')
            else:
                amenity = AmenitiesForm(instance=get_object_or_404(Amenities,pk=pk))
                a = get_object_or_404(Amenities,pk=pk)
                return render(request,'custom_admin/amenities/edit_amenity.html',{'amenity':amenity,'a':a})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def delete_amenity(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            amenity_obj = get_object_or_404(Amenities,pk=pk)
            amenity_obj.delete()
            return redirect('Custom_Admin:all_amenities')
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')



def all_events(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User,pk=request.user.id)
        if user.has_perm('Events.manage_events_and_tickets'):
            events = Events.objects.all()
            events = sorted(events,key=lambda e:e.from_date)
            return render(request,'custom_admin/events/all_events.html',{'events':events})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def add_event(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Events.manage_events_and_tickets'):
            amenity = Amenities.objects.all()
            return render(request,'custom_admin/events/add_event.html',{'amenity':amenity})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def view_event(request,event):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Events.manage_events_and_tickets'):
            event = get_object_or_404(Events,pk=event)
            return render(request,'custom_admin/events/view_event.html',{'event':event})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def edit_event(request,event):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Events.manage_events_and_tickets'):
            if request.method == 'POST':
                event_obj = EventForm(request.POST or None, request.FILES or None,instance=get_object_or_404(Events, pk=event))
                if event_obj.is_valid():
                    event_obj.save()
                    return redirect('Custom_Admin:all_events')
            else:
                amenities = Amenities.objects.filter(amenity_type="A1")
                event = get_object_or_404(Events, pk=event)
                amenity_id = event.amenity.id
                event_form = EventForm(instance=get_object_or_404(Events,pk=event.id))
                return render(request, 'custom_admin/events/edit_event.html', {'event': event,'amenities':amenities,'amenity_id':amenity_id,'event_form':event_form})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def delete_event(request,event):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Events.manage_events_and_tickets'):
            event_obj = get_object_or_404(Events,pk=event)
            event_obj.delete()
            return redirect('Custom_Admin:all_events')
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')


def all_inquiries(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User,pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            inquiries = Inquiry.objects.all()
            inquiries = sorted(inquiries,key=lambda i:i.created_at, reverse=True)
            no_of_inquiries = len(inquiries)
            return render(request,'custom_admin/inquiry/all_inquiries.html',{'inquiries':inquiries,'no_of_inquiries':no_of_inquiries})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def reply_inquiry(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            if request.method == 'POST':
                inquiry_obj = get_object_or_404(Inquiry, pk=pk)
                inquiry_obj.reply = request.POST['reply']
                inquiry_obj.save()
                reply = request.POST['reply']

                subject = "Reply : to your Inquiry from Hawk Club"
                message = "Your Inquiry :-\n" + inquiry_obj.message + "\n\nReply to your Inquiry :-\n" + reply
                email_from = settings.EMAIL_HOST_USER
                email_to = [inquiry_obj.email, ]
                send_mail(subject, message, email_from, email_to)

                return redirect('Custom_Admin:all_inquiries')
            else:
                inquiry = get_object_or_404(Inquiry,pk=pk)
                return render(request,'custom_admin/inquiry/reply_inquiry.html',{'inquiry':inquiry})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def delete_inquiry(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            inquiry_obj = Inquiry(request,pk=pk)
            inquiry_obj.delete()
            return redirect('Custom_Admin:all_inquiries')
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')






def all_feedbacks(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            feedbacks = Feedback.objects.all()
            feedbacks = sorted(feedbacks,key=lambda f:f.given_at, reverse=True)

            avg_overall_experience = 0
            avg_timely_response = 0
            avg_overall_satisfaction = 0
            avg_our_support = 0
            avg_member_service = 0

            no_of_objects = len(feedbacks)

            for f in feedbacks:
                avg_overall_experience = avg_overall_experience + int(f.rating[0])
                avg_timely_response = avg_timely_response + int(f.rating[2])
                avg_our_support = avg_our_support + int(f.rating[4])
                avg_overall_satisfaction = avg_overall_satisfaction + int(f.rating[6])
                avg_member_service = avg_member_service + int(f.rating[8])

            avg_overall_experience = avg_overall_experience / ( 5 * no_of_objects) * 100
            avg_timely_response = avg_timely_response / ( 5 * no_of_objects) * 100
            avg_overall_satisfaction = avg_overall_satisfaction / ( 5 * no_of_objects) * 100
            avg_our_support = avg_our_support / ( 5 * no_of_objects) * 100
            avg_member_service = avg_member_service / ( 5 * no_of_objects) * 100

            avg_all = (avg_member_service + avg_our_support + avg_overall_satisfaction + avg_timely_response + avg_overall_experience)/5

            return render(request,'custom_admin/feedback/all_feedbacks.html',{'feedbacks':feedbacks,'overall_experience':round(avg_overall_experience,2),'timely_response':round(avg_timely_response,2),'our_support':round(avg_our_support,2),'overall_satisfaction':round(avg_overall_satisfaction,2),'member_service':round(avg_member_service,2),'avg_all':round(avg_all,2),'no_of_feedbacks':no_of_objects})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')


def view_feedback(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            feedback = get_object_or_404(Feedback,pk=pk)
            return render(request,'custom_admin/feedback/view_feedback.html',{'feedback':feedback})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def delete_feedback(request,pk):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Inquiry.manage_inquiries_and_feedbacks'):
            feedback_obj = get_object_or_404(Feedback,pk=pk)
            feedback_obj.delete()
            return redirect('Custom_Admin:all_feedbacks')
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')


def all_payments(request):
    if request.user.is_superuser:
        payments = Payments.objects.all()
        payments = sorted(payments,key=lambda p:p.date, reverse=True)
        no_of_payments = len(payments)
        return render(request,'custom_admin/payments/all_payments.html',{'payments':payments,'no_of_payments':no_of_payments})
    else:
        return redirect('Custom_Admin:admin_login')

def download_invoice(request,pk):
    if request.user:
        payment_obj = get_object_or_404(Payments,pk=pk)
        return render(request,'custom_admin/payments/download_invoice.html',{'payment':payment_obj})

def render_to_pdf(template_src,context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),result)

    # if not pdf.err:
    #     return HttpResponse(result.getvalue(),content_type='application/pdf')
    # return None

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

class View_Invoice(View):
    def get(self, request, pk):
        payment_obj = get_object_or_404(Payments,pk=pk)

        if payment_obj.payment_for == "P":

            data = {
                "invoice_id": payment_obj.invoice_id,
                "date": payment_obj.date,
                "member_name": payment_obj.member.member.first_name + " " + payment_obj.member.member.last_name,
                "member_phone": payment_obj.member.phone,
                "member_email": payment_obj.member.member.email,
                "plan": payment_obj.membership.mem_plan.name,
                "duration": payment_obj.membership.mem_plan.duration,
                "amount": payment_obj.amount,
                "payment_status": payment_obj.status,
                "fees": payment_obj.membership.mem_plan.fees,
                "payment_for" : payment_obj.payment_for,
            }

            template_src = 'custom_admin/payments/view_invoice_plan.html'
            context_dict = data
            template = get_template(template_src)
            html = template.render(context_dict)
            result = BytesIO()

            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            name = "invoice_plan"

        elif payment_obj.payment_for == "E":

            data = {
                "invoice_id": payment_obj.invoice_id,
                "date": payment_obj.date,
                "member_name": payment_obj.member.member.first_name + " " + payment_obj.member.member.last_name,
                "member_phone": payment_obj.member.phone,
                "member_email": payment_obj.member.member.email,
                "event": payment_obj.ticket.event.name,
                "ticket_price":payment_obj.ticket.event.price,
                "from": payment_obj.ticket.event.from_date,
                "to": payment_obj.ticket.event.to_date,
                "quantity": payment_obj.ticket.quantity,
                "amount": payment_obj.amount,
                "payment_status": payment_obj.status,
                "payment_for": payment_obj.payment_for,
            }

            template_src = 'custom_admin/payments/view_invoice_ticket.html'
            context_dict = data
            template = get_template(template_src)
            html = template.render(context_dict)
            result = BytesIO()

            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            name = "invoice_ticket"

        elif payment_obj.payment_for == "B":
            data = {
                "invoice_id": payment_obj.invoice_id,
                "date": payment_obj.date,
                "member_name": payment_obj.member.member.first_name + " " + payment_obj.member.member.last_name,
                "member_phone": payment_obj.member.phone,
                "member_email": payment_obj.member.member.email,
                "amenity": payment_obj.booking.amenity.name,
                "amenity_rate": payment_obj.booking.amenity.rate,
                "from": payment_obj.booking.from_date,
                "from2": payment_obj.booking.from_time,
                "to": payment_obj.booking.to_date,
                "to2": payment_obj.booking.to_time,
                "no_of_slots": payment_obj.booking.no_of_slots,
                "amount": payment_obj.amount,
                "payment_status": payment_obj.status,
                "payment_for": payment_obj.payment_for,
            }

            template_src = 'custom_admin/payments/view_invoice_booking.html'
            context_dict = data
            template = get_template(template_src)
            html = template.render(context_dict)
            result = BytesIO()

            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            name = "invoice_booking"

        if not pdf.err:
            pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
            pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
            return pdf
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def all_members(request):
    if request.user.is_superuser:
        membership = Membership.objects.filter(is_expired=False)
        membership = sorted(membership,key=lambda m:m.member.created_at, reverse=True)
        return render(request,'custom_admin/members/all_members.html',{'membership':membership})
    else:
        return redirect('Custom_Admin:admin_login')


def view_member(request,pk):
    if request.user.is_superuser:
        membership_obj = get_object_or_404(Membership,pk=pk)
        member = get_object_or_404(Member,id=membership_obj.member.id)
        membership = Membership.objects.filter(member=member.id)
        membership = sorted(membership,key=lambda m:m.brought_at, reverse=True)
        return render(request,'custom_admin/members/view_member.html',{'member':member,'membership':membership})
    else:
        return redirect('Custom_Admin:admin_login')

def active_deactive_member(request,pk):
    if request.user.is_superuser:
        member = get_object_or_404(Member,pk=pk)
        if member.member.is_active == True:
            member.member.is_active = False
        elif member.member.is_active == False:
            member.member.is_active = True
        else:
            pass

        member.member.save()

        return redirect('Custom_Admin:view_member',member.id)
    else:
        return redirect('Custom_Admin:admin_login')




def all_tickets(request):
    payments = Payments.objects.filter(payment_for="E")
    payments = sorted(payments,key=lambda p:p.date, reverse=True)
    no_of_tickets = len(payments)
    return render(request,'custom_admin/tickets/all_tickets.html',{'tickets':payments,'no__of_tickets':no_of_tickets})

def view_ticket(request,pk):
    user = get_object_or_404(User, pk=request.user.id)
    if user.has_perm('Events.manage_events_and_tickets'):
        payment = get_object_or_404(Payments,pk=pk)
        return render(request,'custom_admin/tickets/view_ticket.html',{'ticket':payment})
    else:
        pass


def collect_tickets(request,ticket):
    user = get_object_or_404(User, pk=request.user.id)
    if user.has_perm('Events.manage_events_and_tickets'):
        payment = get_object_or_404(Payments,pk=ticket)
        ticket = get_object_or_404(Tickets,pk=payment.ticket.id)

        if ticket.collected == False:
            ticket.collected = True

            subject = "Your have collected your tickets!"
            message = "Hi, " + request.user.first_name + " " + request.user.last_name + ". This is to inform you that your tickets for the Ticket ID : " + payment.invoice_id + ".\n\nThank you!"
            email_from = settings.EMAIL_HOST_USER
            email_to = [payment.member.member.email, ]
            send_mail(subject, message, email_from, email_to)

        else:
            ticket.collected = False

        ticket.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        pass


def bookings(request):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User,pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            bookings = Bookings.objects.filter(status=True,confirm=True)
            return render(request,'custom_admin/amenities/bookings.html',{'bookings':bookings})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def view_booking(request,booking):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=request.user.id)
        if user.has_perm('Amenities.view_booking'):
            booking = get_object_or_404(Bookings,pk=booking)
            payment = get_object_or_404(Payments,booking=booking)
            return render(request,'custom_admin/amenities/view_booking.html',{'booking':booking,'payment':payment})
        else:
            pass
    else:
        return redirect('Custom_Admin:admin_login')

def booking_requests(request):
    bookings = Bookings.objects.filter(status=False,confirm=False)
    return render(request,'custom_admin/amenities/booking_requests.html',{'bookings':bookings})

def view_booking_request(request,booking):
    booking = get_object_or_404(Bookings,pk=booking)
    return render(request,'custom_admin/amenities/view_booking_request.html',{'booking':booking})

def accept_booking_request(request,booking):
    booking = get_object_or_404(Bookings,pk=booking)
    booking.status = True
    booking.save()

    subject = "Booking Approved"
    message = "Dear " + booking.member.member.first_name + ",\n\nYour booking for the amenity '" + booking.amenity.name + "' is approved." + "\nYou need to make payment to confirm the booking."
    email_from = settings.EMAIL_HOST_USER
    email_to = [booking.member.member.email, ]
    send_mail(subject, message, email_from, email_to)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def generate_payment_report(request):
    if request.method == 'POST':
        start = int(request.POST['from'])
        end = int(request.POST['to'])

        payments = Payments.objects.all()

        if start==0 and end==0:
            data={
                'payments':payments,
                'no_of_payments':len(payments)
            }
        elif start>0 and end==0:
            payments = Payments.objects.all()[start:len(payments)]
            data = {
                'payments': payments,
                'no_of_payments': len(payments)
            }
        elif start==0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments': payments,
                'no_of_payments': len(payments)
            }
        elif start>0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments': payments,
                'no_of_payments': len(payments)
            }

        template_src = 'custom_admin/reports/payment_report.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        name = "payment_report"

        if not pdf.err:
            pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
            pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
            return pdf
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    else:
        pass


def generate_booking_report(request):
    if request.method == 'POST':
        start = int(request.POST['from'])
        end = int(request.POST['to'])

        payments = Payments.objects.filter(payment_for="B")

        if start==0 and end==0:
            data={
                'payments':payments,
            }
        elif start>0 and end==0:
            payments = Payments.objects.all()[start:len(payments)]
            data = {
                'payments':payments,
            }
        elif start==0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }
        elif start>0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }


        template_src = 'custom_admin/reports/booking_report.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        name = "booking_report"

        if not pdf.err:
            pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
            pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
            return pdf
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    else:
        pass

def generate_ticket_report(request):
    if request.method == 'POST':
        start = int(request.POST['from'])
        end = int(request.POST['to'])

        payments = Payments.objects.filter(payment_for="E")

        if start==0 and end==0:
            data={
                'payments':payments,
            }
        elif start>0 and end==0:
            payments = Payments.objects.all()[start:len(payments)]
            data = {
                'payments':payments,
            }
        elif start==0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }
        elif start>0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }


        template_src = 'custom_admin/reports/ticket_report.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        name = "ticket_report"

        if not pdf.err:
            pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
            pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
            return pdf
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    else:
        pass

def generate_member_report(request):
    if request.method == 'POST':
        start = int(request.POST['from'])
        end = int(request.POST['to'])

        payments = Payments.objects.filter(payment_for="P")

        if start==0 and end==0:
            data={
                'payments':payments,
            }
        elif start>0 and end==0:
            payments = Payments.objects.all()[start:len(payments)]
            data = {
                'payments':payments,
            }
        elif start==0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }
        elif start>0 and end>0:
            payments = Payments.objects.all()[start:end]
            data = {
                'payments':payments,
            }


        template_src = 'custom_admin/reports/member_report.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        name = "member_report"

        if not pdf.err:
            pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
            pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
            return pdf
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    else:
        pass


def broadcast(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'custom_admin/broadcast.html')


def select_report(request):
    return render(request,'custom_admin/reports/select_report.html')

def selected_payment_report(request):
    if request.method == 'POST':
        sort_by = request.POST['sort_by']
        payment_for = request.POST['payment_for']
        member_email = request.POST['member_email'].lower()
        from_date = request.POST['from']
        to_date = request.POST['to']


        if payment_for == "all" and member_email == "":
            payments = Payments.objects.all()
        elif payment_for == "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member,member=user.id)
            payments = Payments.objects.filter(member=member.id)
        elif payment_for == "MP" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member,member=user.id)
            payments = Payments.objects.filter(member=member.id, payment_for='P')
        elif payment_for == "AB" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member,member=user.id)
            payments = Payments.objects.filter(member=member.id, payment_for='B')
        elif payment_for == "ET" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member,member=user.id)
            payments = Payments.objects.filter(member=member.id, payment_for='E')
        elif payment_for == "MP" and member_email == "":
            payments = Payments.objects.filter(payment_for='P')
        elif payment_for == "AB" and member_email == "":
            payments = Payments.objects.filter(payment_for='B')
        elif payment_for == "ET" and member_email == "":
            payments = Payments.objects.filter(payment_for='E')
        else:
            payments = Payments.objects.all()

        if from_date != "" and to_date != "":
            payments = payments.filter(date__gte=from_date,date__lte=to_date)

        if sort_by == "latest_date":
            payments = sorted(payments,key=lambda p:p.date ,reverse=True)
        elif sort_by == "lastest_date":
            payments = sorted(payments, key=lambda p: p.date)
        elif sort_by == "amount_high":
            payments = sorted(payments, key=lambda p: p.amount, reverse=True)
        elif sort_by == "amount_low":
            payments = sorted(payments, key=lambda p: p.amount)


        data = {
            'payments': payments,
            'no_of_payments': len(payments)
        }

        template_src = 'custom_admin/reports/payment_report.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        return HttpResponse(html)
        # result = BytesIO()
        #
        # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # name = "payment_report"
        #
        # if not pdf.err:
        #     pdf = HttpResponse(result.getvalue(),content_type='application/pdf')
        #     pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
        #     return pdf
        # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    else:
        return render(request,'custom_admin/reports/selected_payment_report.html')


def selected_member_report(request):
    if request.method == 'POST':
        sort_by = request.POST['sort_by']
        plan = request.POST['plan']
        member_email = request.POST['member_email'].lower()
        from_date = request.POST['from']
        to_date = request.POST['to']

        if plan == "all" and member_email == "":
            membership = Membership.objects.filter(is_expired=False)
        elif plan == "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            membership = Membership.objects.filter(member=member,is_expired=False)
        elif plan != "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            membership = Membership.objects.filter(member=member,mem_plan=plan,is_expired=False)
        elif plan != "all" and member_email == "":
            membership = Membership.objects.filter(mem_plan=plan,is_expired=False)
        else:
            membership = Membership.objects.all(is_expired=False)

        if from_date != "" and to_date != "":
            membership = membership.filter(member__created_at__gte=from_date, member__created_at__lte=to_date)

        if sort_by == "member_name_asc":
            membership = sorted(membership, key=lambda m: m.member.member.first_name)
        elif sort_by == "member_name_desc":
            membership = sorted(membership, key=lambda m: m.member.member.first_name, reverse=True)
        elif sort_by == "latest_date":
            membership = sorted(membership, key=lambda m: m.member.created_at, reverse=True)
        elif sort_by == "lastest_date":
            membership = sorted(membership, key=lambda m: m.member.created_at)
        elif sort_by == "duration_low":
            membership = sorted(membership, key=lambda m: m.mem_plan.duration)
        elif sort_by == "duration_high":
            membership = sorted(membership, key=lambda m: m.mem_plan.duration, reverse=True)



        data = {
            'membership': membership,
        }

        template_src = 'custom_admin/reports/member_report2.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        return HttpResponse(html)
        # result = BytesIO()

        # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # name = "member_report"
        #
        # if not pdf.err:
        #     pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
        #     pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
        #     return pdf
        # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    else:
        plans = Plans.objects.all()
        return render(request,'custom_admin/reports/selected_member_report.html',{'plans':plans})


def selected_booking_report(request):
    if request.method == 'POST':
        sort_by = request.POST['sort_by']
        amenity = request.POST['amenity']
        member_email = request.POST['member_email'].lower()
        from_date = request.POST['from']
        to_date = request.POST['to']

        if amenity == "all" and member_email == "":
            bookings = Bookings.objects.all()
        elif amenity == "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            bookings = Bookings.objects.filter(member=member.id)
        elif amenity != "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            bookings = Bookings.objects.filter(member=member.id,amenity=amenity)
        elif amenity != "all" and member_email == "":
            bookings = Bookings.objects.filter(amenity=amenity)
        else:
            bookings = Bookings.objects.all()

        if from_date != "" and to_date != "":
            bookings = bookings.filter(from_date__gte=from_date, from_date__lte=to_date)

        if sort_by == "near_first":
            bookings = sorted(bookings, key=lambda b: b.from_date)
        elif sort_by == "near_last":
            bookings = sorted(bookings, key=lambda b: b.from_date, reverse=True)
        elif sort_by == "slots_low":
            bookings = sorted(bookings, key=lambda b: b.no_of_slots)
        elif sort_by == "slots_high":
            bookings = sorted(bookings, key=lambda b: b.no_of_slots, reverse=True)
        elif sort_by == "amount_low":
            bookings = sorted(bookings, key=lambda b: int(b.total))
        elif sort_by == "amount_high":
            bookings = sorted(bookings, key=lambda b: int(b.total), reverse=True)


        data = {
            'bookings': bookings,
        }

        template_src = 'custom_admin/reports/booking_report2.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        return HttpResponse(html)
        # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # name = "booking_report"
        #
        # if not pdf.err:
        #     pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
        #     pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
        #     return pdf
        # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    else:
        amenities = Amenities.objects.filter(amenity_type='A1')
        return render(request,'custom_admin/reports/selected_booking_report.html',{'amenities':amenities})


def selected_ticket_report(request):
    if request.method == 'POST':
        sort_by = request.POST['sort_by']
        event = request.POST['event']
        member_email = request.POST['member_email'].lower()
        from_date = request.POST['from']
        to_date = request.POST['to']
        collected = request.POST['collected']

        if event == "all" and member_email == "":
            payments = Payments.objects.filter(payment_for='E')
        elif event == "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            payments = Payments.objects.filter(member=member.id,payment_for='E')
        elif event != "all" and member_email != "":
            user = get_object_or_404(User, email=member_email)
            member = get_object_or_404(Member, member=user.id)
            payments = Payments.objects.filter(member=member.id, payment_for='E',ticket__event__id=event)
        elif event != "all" and member_email == "":
            payments = Payments.objects.filter(payment_for='E',ticket__event__id=event)
        else:
            payments = Payments.objects.filter(payment_for='E')

        if collected == "yes":
            payments = payments.filter(ticket__collected=True)
        elif collected == "no":
            payments = payments.filter(ticket__collected=False)

        if from_date != "" and to_date != "":
            payments = payments.filter(date__gte=from_date, date__lte=to_date)

        if sort_by == "near_first":
            payments = sorted(payments, key=lambda p: p.ticket.event.from_date)
        elif sort_by == "near_last":
            payments = sorted(payments, key=lambda p: p.ticket.event.from_date, reverse=True)
        elif sort_by == "quantity_low":
            payments = sorted(payments, key=lambda p: p.ticket.quantity)
        elif sort_by == "quantity_high":
            payments = sorted(payments, key=lambda p: p.ticket.quantity ,reverse=True)
        elif sort_by == "latest_brought":
            payments = sorted(payments, key=lambda p: p.date, reverse=True)
        elif sort_by == "lastest_brought":
            payments = sorted(payments, key=lambda p: p.date)

        data = {
            'payments': payments,
        }

        template_src = 'custom_admin/reports/ticket_report2.html'
        context_dict = data
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        return HttpResponse(html)
        # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # name = "ticket_report"
        #
        # if not pdf.err:
        #     pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
        #     pdf['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(name)
        #     return pdf
        # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    else:
        events = Events.objects.all()
        return render(request,'custom_admin/reports/selected_ticket_report.html',{'events':events})


def add_staff(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email'].lower()
            password1 = request.POST['password']
            password2 = request.POST['password2']

            user = request.POST['user']

            if password1 == password2:
                if user == "superuser":
                    new_admin = User.objects.create_superuser(email,email,password1)
                    new_admin.first_name = first_name
                    new_admin.last_name = last_name
                    new_admin.save()
                    return redirect('Custom_Admin:dashboard')
                elif user == "staff":
                    role = request.POST['role']
                    if role == "A":
                        new_staff = User.objects.create_user(email,email,password1)
                        new_staff.first_name = first_name
                        new_staff.last_name = last_name
                        new_staff.is_staff = True
                        permission = Permission.objects.get(codename='view_booking')
                        new_staff.user_permissions.add(permission)
                        new_staff.save()
                        return redirect('Custom_Admin:dashboard')
                    elif role == "E":
                        new_staff = User.objects.create_user(email, email, password1)
                        new_staff.first_name = first_name
                        new_staff.last_name = last_name
                        new_staff.is_staff = True
                        permission = Permission.objects.get(codename='manage_events_and_tickets')
                        new_staff.user_permissions.add(permission)
                        new_staff.save()
                        return redirect('Custom_Admin:dashboard')
                    elif role == 'I':
                        new_staff = User.objects.create_user(email, email, password1)
                        new_staff.first_name = first_name
                        new_staff.last_name = last_name
                        new_staff.is_staff = True
                        permission = Permission.objects.get(codename='manage_inquiries_and_feedbacks')
                        new_staff.user_permissions.add(permission)
                        new_staff.save()
                        return redirect('Custom_Admin:dashboard')
            else:
                pass



        else:
            return render(request,'custom_admin/admin/add_admin.html')
    else:
        return redirect('Custom_Admin:admin_login')


@csrf_exempt
def validate_login(request):
    username = request.POST['username'].lower()
    password = request.POST['password']
    email_exists = User.objects.filter(username__iexact=username, is_staff=True).exists()
    password_matches = authenticate(username=username, password=password)

    if email_exists:
        if password_matches:
            data = {
                'is_exists': 'True',
                'password_matches': 'True'
            }
        else:
            data = {
                'is_exists': 'True',
                'password_matches': 'False'
            }
    else:
        data = {
            'is_exists': 'False'
        }
    return JsonResponse(data)

@csrf_exempt
def validate_email(request):

    email = request.POST['username'].lower()
    email_exists = User.objects.filter(username__iexact=email, is_staff=True).exists()

    if email_exists:
        data = {
            'is_exists': 'True',
        }
    else:
        data = {
            'is_exists': 'False',
        }
    return JsonResponse(data)

@csrf_exempt
def validate_otp(request):
    sent_otp = request.session.get('reset_otp')
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