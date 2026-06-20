from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Rented', 'Rented'),
        ('Pending Approval', 'Pending Approval'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='properties/', default='default.jpg')
    
    # NEW FIELD FOR 360 TOUR
    panorama_360 = models.ImageField(upload_to='panoramas/', null=True, blank=True, help_text="Upload an equirectangular 360-degree image")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    ddress = models.CharField(max_length=255, null=True, blank=True)
    map_url = models.URLField(max_length=500, null=True, blank=True, help_text="Link from Google Maps")
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties', null=True, blank=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='managed_listings', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20) # 'user' or 'agent'

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Booking(models.Model):
    # Status Constants for easier logic in views
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Reserved', 'Reserved'),
    ]

    # Core Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    
    # Metadata
    request_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(help_text="User's initial inquiry or requirements")
    
    # Appointment Details
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    
    # Agent/Response Logic
    agent_response = models.TextField(blank=True, null=True, help_text="The reply sent by the agent")
    is_resolved = models.BooleanField(default=False, help_text="True if the agent has processed the request")
    response_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default=PENDING
    )

    class Meta:
        ordering = ['-request_date']
        verbose_name = "Booking/Inquiry"
        verbose_name_plural = "Bookings & Inquiries"

    def __str__(self):
        return f"{self.user.username} - {self.property.title} ({self.response_status})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.role}"