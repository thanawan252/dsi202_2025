from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Equipment
from django.db.models import Q  # For complex queries
from django.views import View  # เพิ่ม View
from django.shortcuts import render, get_object_or_404


# Home Page (FBV)
def home(request):
    return render(request, 'myapp/home.html')

# Favorites Page (FBV)
def fav_view(request):
    #favorite_items = request.user.favorites.all()  # ดึงรายการโปรดของผู้ใช้ปัจจุบัน
    return render(request, 'myapp/fav.html') #, {'favorite_items': favorite_items})

#Cart Page
def cart_view(request):
    cart = request.session.get('cart', [])
    total_price = sum(item['months'] * item['price'] for item in cart)

    return render(request, 'myapp/cart.html', {
        'cart_items': cart,
        'total_price': total_price,
    })

def add_to_cart(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    months = int(request.POST.get('months', 1))
    cart = request.session.get('cart', [])

    cart.append({
        'id': equipment.id,
        'name': equipment.name,
        'months': months,
        'price': float(equipment.rental_price),  # แปลง Decimal เป็น float เพื่อใช้ใน session
        'total': months * float(equipment.rental_price)
    })

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, equipment_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != equipment_id]
    request.session['cart'] = cart
    return redirect('cart')

#  (CBV)
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'myapp/equipment_list.html'
    context_object_name = 'equipments'  # Name of the variable in the template

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-rental_price')  # Get the default queryset
        query = self.request.GET.get('q')  # Get the search term from the URL (e.g., ?q=mountain)
        if query:
            # Filter where name or description contains the query (case-insensitive)
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset
    
#Rental Page
# เปลี่ยนชื่อคลาส rent เป็น RentView ตาม convention
class RentView(View):
    def get(self, request, equipment_id):
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        return render(request, 'myapp/rent.html', {'equipment': equipment})

#(CBV: DetailView)
class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'myapp/equipment_detail.html'
    context_object_name = 'equipment'  # Name of the variable in the template