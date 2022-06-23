from django.urls import path
from . import views

app_name = 'Payments'

urlpatterns=[
    path('process_payment_plan/<int:plan>',views.process_payment_plan, name='process_payment_plan'),
    path('payment_success_plan/',views.payment_success_plan, name='payment_success_plan'),
    path('payment_failed_plan/',views.payment_failed_plan, name='payment_failed_plan'),

    path('process_payment_ticket/<int:event>',views.process_payment_ticket, name='process_payment_ticket'),
    path('payment_success_ticket/',views.payment_success_ticket, name='payment_success_ticket'),

    path('process_payment_booking/<int:booking>',views.process_payment_booking, name='process_payment_booking'),
    path('payment_success_booking/',views.payment_success_booking, name='payment_success_booking'),
]