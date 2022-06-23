from django.shortcuts import render,redirect,get_object_or_404
from .forms import PlanForm
from .models import Plans
# Create your views here.


def add_plans(request):
    if request.method == 'POST':
        plan_form = PlanForm(request.POST or None)
        if plan_form.is_valid():
            plan_form.save()
            return redirect('Custom_Admin:all_plans')
        else:
            pass
    else:
        plan_form = PlanForm()
    return render(request,'plans/add_plan.html',{'plan_form':plan_form})

def view_plans(request):
    plans = Plans.objects.all()
    return render(request,'plans/plans.html',{'plans':plans})

def single_plan(request,plan):
    plan = get_object_or_404(Plans,pk=plan)
    return render(request,'plans/single_plan.html',{'plan':plan})