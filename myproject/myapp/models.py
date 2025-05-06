from django.db import models

class Shopkeeper(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('not available', 'Not available')])
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='equipments/', null=True, blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='rentals')
    quantity = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_returned = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rental {self.id} - {self.user.name}"

class Donation(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name='donations')
    equipment_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('new', 'New'), ('used', 'Used')])
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.equipment_name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name='payment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])

    def __str__(self):
        return f"Payment {self.id} - {self.user.name}"
