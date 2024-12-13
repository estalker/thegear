from django.shortcuts import render
from .models import Item, ItemCategory

# Create your views here.
def items_list(request):
    items = Item.objects.all()

    context = {
        'items':items
    }

    return render(request, 'gearapp/items_list.html', context)

def storage_report(request):
    items = Item.objects.all().order_by('current_storage')

    cities = [{"name": "Mumbai", "population": "19,000,000", "country": "India"},
        {"name": "Calcutta", "population": "15,000,000", "country": "India"},
        {"name": "New York", "population": "20,000,000", "country": "USA"},
        {"name": "Chicago", "population": "7,000,000", "country": "USA"},
        {"name": "Tokyo", "population": "33,000,000", "country": "Japan"}, ]

    context = {'items': items, "cities": cities}

    return render(request, 'gearapp/storage_report.html', context)