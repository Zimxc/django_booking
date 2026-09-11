from django.urls import path

from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('booking/make/', views.make_booking, name='make_booking'),
    path('booking/my/', views.my_bookings, name='my_bookings'),
]
