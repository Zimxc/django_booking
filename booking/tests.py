from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Customer, Room


class BookingViewsTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create_user(
            username='alice',
            password='test-password',
            email='alice@example.com',
            phone_number='+380000000001',
        )
        self.room = Room.objects.create(
            room_number='101',
            room_type='Meeting room',
            price_per_hour='20.00',
            capacity=6,
        )

    def test_room_list_shows_rooms(self):
        response = self.client.get(reverse('room_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 101')

    def test_make_booking_page_shows_rooms(self):
        self.client.force_login(self.customer)

        response = self.client.get(reverse('make_booking'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.room.room_number)

    def test_customer_can_create_booking(self):
        self.client.force_login(self.customer)
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)

        response = self.client.post(reverse('make_booking'), {
            'room_number': self.room.room_number,
            'datetime_start': start.strftime('%Y-%m-%dT%H:%M'),
            'datetime_end': end.strftime('%Y-%m-%dT%H:%M'),
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_success.html')
        self.assertEqual(Booking.objects.count(), 1)

    def test_my_bookings_shows_only_current_customer_bookings(self):
        booking = Booking.objects.create(
            customer=self.customer,
            room=self.room,
            datetime_start=timezone.now() + timedelta(days=1),
            datetime_end=timezone.now() + timedelta(days=1, hours=1),
        )
        self.client.force_login(self.customer)

        response = self.client.get(reverse('my_bookings'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(booking.room))
