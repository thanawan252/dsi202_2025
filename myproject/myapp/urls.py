from django.urls import path
from .views import home, EquipmentListView, EquipmentDetailView, fav_view, RentView, cart_view, add_to_cart, remove_from_cart

urlpatterns = [
    path('', home, name='home'),  # Home page at root URL
    path('equipments/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipments/<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('fav/', fav_view, name='fav'),  # เพิ่ม URL สำหรับหน้า Favorites
    path('rents/create/<int:equipment_id>/', RentView.as_view(), name='rent'),
    path('equipments/<int:equipment_id>/rent.html', RentView.as_view(), name='rent_alt'),
    path('cart/', cart_view, name='cart'),  # หน้า Cart
    path('cart/add/<int:equipment_id>/', add_to_cart, name='add_to_cart'),  # สำหรับการเพิ่มอุปกรณ์ลงในตะกร้า
    path('cart/remove/<int:equipment_id>/', remove_from_cart, name='remove_from_cart'),  # สำหรับการลบอุปกรณ์จากตะกร้า
]