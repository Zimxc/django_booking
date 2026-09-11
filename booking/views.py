from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import Booking, Room


def room_list(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'booking/room_list.html', {'rooms': rooms})


@login_required
def make_booking(request):
    rooms = Room.objects.all().order_by('room_number')

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        datetime_start = parse_datetime(request.POST.get('datetime_start', ''))
        datetime_end = parse_datetime(request.POST.get('datetime_end', ''))
        room = Room.objects.filter(room_number=room_number).first()

        if not room or not datetime_start or not datetime_end:
            return render(request, 'booking/booking_error.html', {
                'error': 'Please select a room and enter valid dates.'
            })

        if timezone.is_naive(datetime_start):
            datetime_start = timezone.make_aware(datetime_start)
        if timezone.is_naive(datetime_end):
            datetime_end = timezone.make_aware(datetime_end)

        if datetime_start >= datetime_end:
            return render(request, 'booking/booking_error.html', {
                'error': 'End time must be later than start time.'
            })

        room_is_busy = Booking.objects.filter(
            room=room,
            datetime_start__lt=datetime_end,
            datetime_end__gt=datetime_start,
        ).exclude(status='cancelled').exists()

        if room_is_busy:
            return render(request, 'booking/booking_error.html', {
                'error': 'Room is already booked for the selected time slot.'
            })

        booking = Booking.objects.create(
            customer=request.user,
            room=room,
            datetime_start=datetime_start,
            datetime_end=datetime_end
        )

        return render(request, 'booking/booking_success.html', {
            'booking': booking
        })

    return render(request, 'booking/make_booking.html', {
        'rooms': rooms,
        'selected_room': request.GET.get('room', ''),
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related('room').order_by('-datetime_start')

    return render(request, 'booking/my_bookings.html', {
        'bookings': bookings
    })
