from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# DON'T FORGET TO MAKE AN ABSTRACT USER MODEL FOR CUSTOMERS
class Customer(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

class Booking(models.Model):
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)


    def __str__(self):
        return f"Booking for {self.customer.username} from {self.datetime_start} to {self.datetime_end}"

class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=50)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    special_features = models.TextField(blank=True)
    capacity = models.IntegerField()
    

    def __str__(self):
        return f"{self.room_type} - {self.room_number}"
