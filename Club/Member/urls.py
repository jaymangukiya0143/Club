from django.urls import path
from . import views

app_name = 'Member'

urlpatterns=[
    path('signup/',views.signup, name='signup'),
    path('login_member/',views.login_member, name='login_member'),
    path('logout_member/',views.logout_member, name='logout_member'),
    path('email_otp_verification/',views.email_otp_verification, name='email_otp_verification'),
    path('change_password/',views.change_password, name='change_password'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset_otp/',views.reset_otp, name='reset_otp'),

    path('profile/',views.profile, name='profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),

    path('validate_email/',views.validate_email, name='validate_email'),
    path('validate_email_signup',views.validate_email_signup, name='validate_email_signup'),
    path('validate_otp/<int:req_from>',views.validate_otp, name='validate_otp'),
    path('validate_password/',views.validate_password, name='validate_password'),

    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('view_booking/<int:booking>', views.view_booking, name='view_booking'),
    path('send_booking_request/<int:pk>',views.send_booking_request, name='send_booking_request'),
    path('booking_request/',views.booking_request, name='booking_request'),

    path('my_tickets', views.my_tickets, name='my_tickets'),
    path('view_ticket/<int:payment>', views.view_ticket, name='view_ticket'),

    path('my_payments', views.my_payments, name='my_payments'),
    path('view_payment/<int:payment>', views.view_payment, name='view_payment'),

    path('my_plans', views.my_plans, name='my_plans'),
    path('view_plan/<int:pk>', views.view_plan, name='view_plan'),
]