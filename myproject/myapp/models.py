# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from decimal import Decimal
from datetime import timedelta

# User Type Choices
USER_TYPE_CHOICES = (
    ('renter', 'Renter'),
    ('donater', 'Donater'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='renter')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    monthly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.is_available = self.stock > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Simple 1-5 star rating
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"

    class Meta:
        ordering = ['-created_at']

class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # Prevent multiple likes from the same user

    def __str__(self):
        return f"{self.user.username} likes {self.review}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField(default=now, null=True)
    rental_months = models.PositiveIntegerField(default=1, help_text="Number of months for rental (1-12)")
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[
        ('preparing', 'Preparing'),
        ('ongoing', 'Ongoing'),
        ('returning', 'Returning'),
        ('returned', 'Returned'),
    ], default='preparing')
    created_at = models.DateTimeField(auto_now_add=True)
    last_payment_reminder = models.DateTimeField(null=True, blank=True)

    def calculate_total_fee(self):
        monthly_rate = self.product.monthly_rate
        total_fee = monthly_rate * Decimal(str(self.rental_months))
        return total_fee.quantize(Decimal('0.01'))

    def get_end_date(self):
        if not self.start_date:
            return None
        days = self.rental_months * 30
        return self.start_date + timedelta(days=days)

    def remaining_months(self):
        if not self.start_date or self.status == 'returned':
            return 0
        today = now().date()
        end_date = self.get_end_date()
        if today >= end_date:
            return 0
        days_left = (end_date - today).days
        return max(1, (days_left + 29) // 30)

    def needs_payment_reminder(self):
        if self.status != 'ongoing' or not self.start_date:
            return False
        today = now()
        days_since_start = (today.date() - self.start_date).days
        if not self.last_payment_reminder:
            return days_since_start >= 25
        days_since_last_reminder = (today - self.last_payment_reminder).days
        return days_since_last_reminder >= 25

    def save(self, *args, **kwargs):
        self.total_fee = self.calculate_total_fee()
        if not self.pk:
            if self.product.stock > 0:
                self.product.stock -= 1
                self.product.save()
        else:
            old_rental = Rental.objects.get(pk=self.pk)
            if self.status == 'returned' and old_rental.status != 'returned':
                self.product.stock += 1
                self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.status})"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} donated {self.product_name}"
