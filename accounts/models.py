from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    
    ADVANTAGE_LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    advantage_level = models.CharField(max_length=10, choices=ADVANTAGE_LEVELS, default='bronze')
    total_bookings = models.PositiveIntegerField(default=0, help_text="Total restaurant reservations made")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Automatically set role to 'admin' for superusers
        if self.is_superuser or self.is_staff:
            self.role = 'admin'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def update_advantage_level(self):
        """Update user advantage level based on total reservations"""
        if self.total_bookings >= 20:
            self.advantage_level = 'platinum'
        elif self.total_bookings >= 10:
            self.advantage_level = 'gold'
        elif self.total_bookings >= 5:
            self.advantage_level = 'silver'
        else:
            self.advantage_level = 'bronze'
        self.save()
    
    def get_discount_percentage(self):
        """Get discount percentage based on advantage level for reservation fees"""
        discounts = {
            'bronze': 0,
            'silver': 5,
            'gold': 10,
            'platinum': 15,
        }
        return discounts.get(self.advantage_level, 0)