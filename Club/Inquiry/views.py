from django.shortcuts import render,redirect,get_object_or_404
from Club import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import *

# Create your views here.

def inquiry(request):
    if request.method == "POST":
        form = InquiryForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            sub = form.cleaned_data['subject']
            content = form.cleaned_data['message']

            form.save()
            subject = 'Hello ' + name + ' from Hawk Club!'
            message = "Your Inquiry :- \n{} is submitted and Our team will reply as soon as possible. \n\nStay Connected. We would love to hear you!".format(content)
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)
            messages.success(request, 'Form submitted successfully.')
            return redirect('Home:home')
        else:
            # messages.error(request, 'Please correct the error below.')
            pass
    else:
        form = InquiryForm()
    return render(request, 'inquiry/inquiry.html', {'form': form})


def view_inquiries(request):
    inquiries = Inquiry.objects.all()
    return render(request,'inquiry/view_inquiries.html',{'inquiries':inquiries})


def single_inquiry(request,pk):
    inquiry = get_object_or_404(Inquiry,pk=pk)
    return render(request,'inquiry/single_inquiry.html',{'inquiry':inquiry})

def send_reply(request,pk):
    if request.method == 'POST':
        inquiry_obj = get_object_or_404(Inquiry,pk=pk)
        inquiry_obj.reply = request.POST['reply']
        inquiry_obj.save()
        reply = request.POST['reply']

        subject = "Reply : to your Inquiry from Hawk Club"
        message = "Your Inquiry :-\n" + inquiry_obj.message + "\n\nReply to your Inquiry :-\n" + reply
        email_from = settings.EMAIL_HOST_USER
        email_to = [inquiry_obj.email, ]
        send_mail(subject, message, email_from, email_to)
        messages.success(request, 'Form submitted successfully.')
        return redirect('Inquiry:view_inquiries')