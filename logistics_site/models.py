from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Shipment(models.Model):
    
    driver = models.ForeignKey(
    User, on_delete=models.SET_NULL, null=True, blank=True,
    related_name='deliveries', limit_choices_to={'role': 'driver'}
   )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed Delivery'),
        ('cancelled', 'Cancelled'),
    ]    
    
    tracking_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')

    sender_name = models.CharField(max_length=200)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=20,null=True, blank=True)
    

    recipient_name = models.CharField(max_length=200)
    recipient_address = models.TextField()
    recipient_phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    location = models.CharField(max_length=200, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.tracking_number

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            import uuid
            self.tracking_number = 'TRK' + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)
        
class ShipmentEvent(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status}" 
    
class Enquiry(models.Model):
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    pickup_state = models.CharField(max_length=100)
    cargo_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company or 'Unknown company'} — {self.email}"    