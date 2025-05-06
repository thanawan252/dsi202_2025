from django.contrib import admin
from .models import Shopkeeper, Equipment, User, Rental, Donation, Payment

@admin.register(Shopkeeper)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address')
    search_fields = ('name', 'email')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'rental_price', 'stock', 'image')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address')
    search_fields = ('name', 'email')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'quantity', 'start_date', 'end_date', 'is_returned', 'total_price')
    list_filter = ('is_returned',)
    search_fields = ('user__name', 'equipment__name')