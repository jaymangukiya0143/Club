from django.urls import path
from . import views

app_name = 'Events'

urlpatterns=[
    path('add_event/',views.add_event, name='add_event'),
    path('view_events/',views.view_events, name='view_events'),

    path('buy_tickets/<int:pk>',views.buy_tickets, name='buy_tickets'),
]