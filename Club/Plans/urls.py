from django.urls import path
from . import views

app_name = 'Plans'

urlpatterns = [
    path('add_plans/',views.add_plans, name='add_plans'),
    path('view_plans/',views.view_plans, name='view_plans'),
    path('single_plan/<int:plan>', views.single_plan, name='single_plan'),
]