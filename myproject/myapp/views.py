from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Equipment
from django.db.models import Q  # For complex queries

# Home Page (FBV)
def home(request):
    return render(request, 'myapp/home.html')

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

#(CBV: DetailView)
class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'myapp/equipment_detail.html'
    context_object_name = 'equipment'  # Name of the variable in the template