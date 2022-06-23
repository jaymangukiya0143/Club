from django.urls import path
from . import views
from .views import View_Invoice
from django.views.generic import TemplateView

app_name = 'Custom_Admin'

urlpatterns=[
    path('dashboard/',views.dashboard, name='dashboard'),
    path('admin_login/',views.admin_login, name='admin_login'),
    path('admin_logout/',views.admin_logout, name='admin_logout'),
    path('profile/',views.profile, name='profile'),
    path('forgot_password/',views.admin_forgot_password, name='admin_forgot_password'),
    path('reset_password/',views.admin_reset_password, name='admin_reset_password'),
    path('change_password/',views.admin_change_password, name='admin_change_password'),


    path('all_plans/',views.all_plans, name='all_plans'),
    path('add_plan/',views.add_plan, name='add_plan'),
    path('view_plan/<int:pk>',views.view_plan, name='view_plan'),
    path('edit_plan/<int:pk>',views.edit_plan, name='edit_plan'),
    path('delete_plan/<int:pk>',views.delete_plan, name='delete_plan'),

    path('all_amenities/',views.all_amenities, name='all_amenities'),
    path('add_amenity/',views.add_amenity, name='add_amenity'),
    path('view_amenity/<int:pk>',views.view_amenity, name='view_amenity'),
    path('edit_amenity/<int:pk>',views.edit_amenity, name='edit_amenity'),
    path('delete_amenity/<int:pk>',views.delete_amenity, name='delete_amenity'),

    path('all_events/',views.all_events, name='all_events'),
    path('add_event/',views.add_event, name='add_event'),
    path('view_event/<int:event>',views.view_event, name='view_event'),
    path('edit_event/<int:event>',views.edit_event, name='edit_event'),
    path('delete_event/<int:event>',views.delete_event, name='delete_event'),


    path('all_inquiries/',views.all_inquiries, name='all_inquiries'),
    path('reply_inquiry/<int:pk>',views.reply_inquiry, name='reply_inquiry'),
    path('delete_inquiry/<int:pk>',views.delete_inquiry, name='delete_inquiry'),


    path('all_feedbacks/',views.all_feedbacks, name='all_feedbacks'),
    path('view_feedback/<int:pk>',views.view_feedback, name='view_feedback'),
    path('delete_feedback/<int:pk>',views.delete_feedback, name='delete_feedback'),

    path('all_payments/',views.all_payments, name='all_payments'),
    path('view_invoice/<int:pk>',views.View_Invoice.as_view(), name='view_invoice'),
    path('download_invoice/<int:pk>',views.download_invoice ,name='download_invoice'),

    path('all_members/',views.all_members, name='all_members'),
    path('view_member/<int:pk>',views.view_member, name='view_member'),
    path('active_deactive_member/<int:pk>',views.active_deactive_member, name='active_deactive_member'),

    path('all_tickets/',views.all_tickets, name='all_tickets'),
    path('view_ticket/<int:pk>',views.view_ticket, name='view_ticket'),
    path('collect_tickets/<int:ticket>',views.collect_tickets, name='collect_tickets'),

    path('booking_requests/',views.booking_requests, name='booking_requests'),
    path('view_booking_request/<int:booking>', views.view_booking_request, name='view_booking_request'),
    path('bookings',views.bookings ,name='bookings'),
    path('view_booking/<int:booking>', views.view_booking, name='view_booking'),
    path('accept_booking_request/<int:booking>', views.accept_booking_request, name='accept_booking_request'),


    path('select_report/',views.select_report, name='select_report'),
    path('selected_payment_report/',views.selected_payment_report, name='selected_payment_report'),
    path('selected_member_report/',views.selected_member_report, name='selected_member_report'),
    path('selected_booking_report/',views.selected_booking_report, name='selected_booking_report'),
    path('selected_ticket_report/',views.selected_ticket_report, name='selected_ticket_report'),
    path('generate_payment_report',views.generate_payment_report, name='generate_payment_report'),
    path('generate_booking_report', views.generate_booking_report, name='generate_booking_report'),
    path('generate_ticket_report', views.generate_ticket_report, name='generate_ticket_report'),
    path('generate_member_report', views.generate_member_report, name='generate_member_report'),


    path('broadcast/',views.broadcast, name='broadcast'),

    path('add_staff/',views.add_staff, name='add_staff'),

    path('validate_login/', views.validate_login, name = 'validate_login'),
    path('validate_email/',views.validate_email, name='validate_email'),
    path('validate_otp/',views.validate_otp, name='validate_otp'),
    path('validate_password/',views.validate_password, name='validate_password'),

]
