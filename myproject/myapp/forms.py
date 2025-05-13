# myapp/forms.py
from django import forms
from .models import Rental, UserProfile, Donation, Review, USER_TYPE_CHOICES

class RentalForm(forms.ModelForm):
    rental_months = forms.ChoiceField(
        choices=[(i, f"{i}") for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
    )

    class Meta:
        model = Rental
        fields = ['start_date', 'rental_months']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'last_name', 'address', 'user_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'address': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'user_type': forms.Select(choices=USER_TYPE_CHOICES, attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['product_name', 'description', 'image']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)], attrs={'class': 'w-full p-3 border border-[#009aa6] rounded-lg'}),
        }