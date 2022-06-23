from django.urls import path
from . import views

app_name = 'Amenities'

urlpatterns=[
    path('add_amenity/',views.add_amenity, name='add_amenity'),
    path('amenities/',views.amenities, name='amenities'),
    path('activities/',views.activities, name='activities'),
    path('single_amenity/<int:pk>',views.single_amenity, name='single_amenity'),
    path('book_amenity/<int:pk>',views.book_amenity, name='book_amenity'),

]