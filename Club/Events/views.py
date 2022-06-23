from django.shortcuts import render,redirect,get_object_or_404
from .models import Events

from Member.views import check_eligiblity
from django.contrib.auth.models import User

from Member.models import Member,Membership

# Create your views here.


def add_event(request):
    if request.method == 'POST':
        event_form = Events()
        event_form.name = request.POST['name']
        event_form.description = request.POST['description']
        event_form.from_date = request.POST['from_date']
        event_form.to_date = request.POST['to_date']
        event_form.capacity = request.POST['capacity']
        event_form.price = request.POST['price']
        event_form.image1 = request.POST['image1']

        event_form.save()
        return redirect('Home:home')
    else:
        return render(request,'events/add_event.html')

def view_events(request):
    events = Events.objects.all()
    events = sorted(events,key=lambda e:e.id,reverse=True)

    return render(request,'events/events.html',{'events':events})


def buy_tickets(request,pk):
    if request.user:

        user = get_object_or_404(User, id=request.user.id)
        member_obj = get_object_or_404(Member, member=user)

        eligible = check_eligiblity(member_obj)

        if eligible:
            event = get_object_or_404(Events,pk=pk)
            return render(request,'events/buy_tickets.html',{'event':event})
        else:
            memberships = Membership.objects.filter(member__member=request.user.id)
            return render(request, 'member/renew_plan/renew_plan.html', {'membership': memberships})
    else:
        return redirect('Member:login_member')