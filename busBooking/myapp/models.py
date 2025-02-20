# Create your models here.
from django.db import models
from decimal import Decimal


# Create your models here.

class Bus(models.Model):
    SEAT_CLASS_CHOICES = [
        ('GEN', 'General'),
        ('SLP', 'Sleeper'),
        ('LUX', 'Luxury'),
    ]
    
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    seat_class = models.CharField(max_length=3, choices=SEAT_CLASS_CHOICES, default='GEN')
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    
    class Meta:
        verbose_name_plural = "List of Busses"

    def __str__(self):
        return f"{self.bus_name} - {self.get_seat_class_display()}"
    def get_price_by_class(self):
        """Return the price adjusted by seat class"""
        if self.seat_class == 'SLP':
            return self.price * Decimal('1.5')  # 50% more for sleeper
        elif self.seat_class == 'LUX':
            return self.price * Decimal('2.0')  # Double price for luxury
        return self.price  # Default price for general


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "List of Users"

    def __str__(self):
        return self.email
    



class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
                       
    SEAT_CLASS_CHOICES = [
        ('GEN', 'General'),
        ('SLP', 'Sleeper'),
        ('LUX', 'Luxury'),
    ]
                       
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid = models.DecimalField(decimal_places=0, max_digits=2)
    busid = models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    seat_class = models.CharField(max_length=3, choices=SEAT_CLASS_CHOICES, default='GEN')
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    


from django.contrib.auth.models import User as AuthUser

class Wallet(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wallet - Balance: ₹{self.balance}"

    def add_funds(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def deduct_funds(self, amount):
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

