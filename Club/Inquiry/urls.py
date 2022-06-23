from django.urls import path
from . import views

app_name='Inquiry'

urlpatterns=[
    path('inquiry/',views.inquiry, name='inquiry'),
    path('view_inquiries/',views.view_inquiries, name='view_inquiries'),
    path('single_inquiry/<int:pk>',views.single_inquiry, name='single_inquiry'),
    path('send_reply/<int:pk>',views.send_reply, name='send_reply'),
]