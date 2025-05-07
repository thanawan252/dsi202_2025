# /myproject/myapp/urls.py
from django.urls import path
from .views import home, EquipmentListView, EquipmentDetailView, fav_view

urlpatterns = [
    path('', home, name='home'),  # Home page at root URL
    path('equipments/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipments/<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('fav/', fav_view, name='fav'),  # เพิ่ม URL สำหรับหน้า Favorites
]