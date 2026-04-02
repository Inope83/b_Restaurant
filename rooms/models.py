from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()

class TableType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base reservation fee")
    max_capacity = models.PositiveIntegerField()
    features = models.TextField(help_text="Comma-separated list of features (e.g., Window view, Private, VIP)")
    
    def __str__(self):
        return self.name

class Table(models.Model):
    TABLE_STATUS = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    table_number = models.CharField(max_length=10, unique=True)
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name='tables')
    location = models.CharField(max_length=50, help_text="e.g., Main Hall, Terrace, Private Room")
    status = models.CharField(max_length=15, choices=TABLE_STATUS, default='available')
    description = models.TextField(blank=True)
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['location', 'table_number']
    
    def __str__(self):
        return f"Table {self.table_number} - {self.table_type.name}"
    
    def is_available(self, reservation_date, reservation_time, duration_hours=2):
        """Check if table is available for given date and time"""
        from datetime import datetime, timedelta
        
        # Convert to datetime for comparison
        start_time = datetime.combine(reservation_date, reservation_time)
        end_time = start_time + timedelta(hours=duration_hours)
        
        overlapping_reservations = self.reservations.filter(
            status__in=['confirmed', 'seated'],
            reservation_date=reservation_date,
            reservation_time__lt=end_time.time(),
            end_time__gt=start_time.time()
        )
        return not overlapping_reservations.exists() and self.status == 'available'

class TableImage(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='table_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"Image for {self.table.table_number}"

class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    end_time = models.TimeField(help_text="Expected end time of reservation")
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=RESERVATION_STATUS, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    special_requests = models.TextField(blank=True, help_text="Dietary restrictions, special occasions, etc.")
    reservation_reference = models.CharField(max_length=20, unique=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reservation {self.reservation_reference} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_reference:
            import uuid
            self.reservation_reference = str(uuid.uuid4())[:8].upper()
        
        # Calculate end time if not provided (default 2 hours)
        if not self.end_time:
            from datetime import datetime, timedelta
            start_datetime = datetime.combine(self.reservation_date, self.reservation_time)
            end_datetime = start_datetime + timedelta(hours=2)
            self.end_time = end_datetime.time()
        
        # Calculate total amount (reservation fee)
        base_amount = self.table.reservation_fee
        
        # Apply discount based on user advantage level
        discount_percentage = self.user.get_discount_percentage()
        self.discount_amount = base_amount * Decimal(discount_percentage / 100)
        self.final_amount = base_amount - self.discount_amount
        self.total_amount = base_amount
        
        super().save(*args, **kwargs)
        
        # Update user's total reservations and advantage level
        if self.status == 'confirmed' and self._state.adding:
            self.user.total_bookings += 1
            self.user.update_advantage_level()
    
    @property
    def duration_hours(self):
        from datetime import datetime, timedelta
        start_datetime = datetime.combine(self.reservation_date, self.reservation_time)
        end_datetime = datetime.combine(self.reservation_date, self.end_time)
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        duration = end_datetime - start_datetime
        return duration.total_seconds() / 3600

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment {self.amount} for {self.reservation.reservation_reference}"