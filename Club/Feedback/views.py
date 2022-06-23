from django.shortcuts import render,redirect,get_object_or_404
from .models import Feedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Club import settings
from django.contrib import messages
from django.core.mail import send_mail

from Member.views import check_eligiblity
from Member.models import Member,Membership

# Create your views here.


@login_required()
def give_feedback(request):
    member = request.user
    if request.method == 'POST':

        user = get_object_or_404(User, id=request.user.id)
        member_obj = get_object_or_404(Member, member=user)

        eligible = check_eligiblity(member_obj)

        if eligible:
            feedback_form = Feedback()

            feedback_form.member = request.user
            feedback_form.feedback = request.POST.get('feedback')
            ratings = request.POST.get('inlineRadioOptions1') +","+request.POST['inlineRadioOptions2']+","+request.POST['inlineRadioOptions3']+","+request.POST['inlineRadioOptions4']+","+request.POST['inlineRadioOptions5']
            print(ratings)
            feedback_form.rating = ratings
            feedback_form.save()

            subject = "Your Feedback given successfully, "+request.user.username
            message = "\n\nThank you for giving feedback. It will help us to make our services better."
            email_from = settings.EMAIL_HOST_USER
            email_to = [request.user.email,]
            send_mail(subject,message,email_from,email_to)
            return redirect('Home:home')
        else:
            memberships = Membership.objects.filter(member__member=request.user.id)
            return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})
    else:
        pass
    return render(request,'feedback/give_feedback.html',{'member':member})