from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics
from .models import Item, ItemCategory, MainCategory, Mission, MissionItem
from .serializers import ItemSerializer
from django.contrib.auth.forms import UserCreationForm
from .forms import MissionForm
import re
from collections import defaultdict

# Create your views here.
def items_list(request):
    items = []
    if request.user.id is not None:
        items = Item.objects.all().select_related("item_category").select_related("item_category__maincategory").filter(item_category__maincategory__user_id=request.user)

    context = {
        'items':items,
    }

    return render(request, 'gearapp/items_list.html', context)


def current_storage(request):
    items = []
    if request.user.id is not None:
        items = Item.objects.all().select_related("item_category").select_related("item_category__maincategory").filter(item_category__maincategory__user_id=request.user).order_by('current_storage')
    context = {'items': items}

    return render(request, 'gearapp/current_storage.html', context)


def usual_storage(request):
    items = []
    if request.user.id is not None:
        items = Item.objects.all().select_related("item_category").select_related("item_category__maincategory").filter(item_category__maincategory__user_id=request.user).order_by('last_storage')
    context = {'items': items}

    return render(request, 'gearapp/usual_storage.html', context)

def missions_list(request):
    missions = []
    if request.user.id is not None:
        missions = Mission.objects.all().filter(user_id=request.user).order_by('-date_start')
    context = {'missions': missions}

    return render(request, 'gearapp/missions_list.html', context)


def mission_create_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = MissionForm(request.POST or None)

    if form.is_valid():
        #form.data["user"] = request.user
        # form.save()
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return render(request, "gearapp/missions_list.html", context)


    context['form'] = form
    return render(request, "gearapp/mission_create_view.html", context)


def parse_post_data(post_data):
    result = defaultdict(lambda: defaultdict(list))  # Многомерный словарь для вложенных данных
    pattern = r'^col\[(\d+)\]\[items\]\[(\d+)\]$'  # Регулярное выражение для извлечения индексов

    for key, value in post_data.items():
        match = re.match(pattern, key)
        if match:
            col_index = int(match.group(1))  # Индекс колонки
            item_index = int(match.group(2))  # Индекс элемента
            result[col_index][item_index] = value

    return result

def mission_view(request, id):
    context={}

    if request.method == 'POST':
        if request.user.id is not None:
            form = MissionForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.id = id
                obj.user = request.user
                obj.save()

                MissionItem.objects.filter(mission_id = id).delete()

                cols = parse_post_data(request.POST)
                for col_index, items in cols.items():
                    storage = MissionItem()
                    storage.mission_id = id
                    storage.item_id = col_index
                    storage.save()
                    for item_index, value in items.items():
                        mi = MissionItem()
                        mi.mission_id = id
                        mi.item_id = value
                        mi.storage_id = storage.id
                        mi.save()





    if request.user.id is not None:
        mission = Mission.objects.all().filter(user_id=request.user).get(id=id)
        context["data"] = mission

        lug_cat = MainCategory.objects.all().filter(user_id=request.user).filter(name = 'Luggage')[:1].get()
        all_items = Item.objects.all().select_related("item_category").select_related("item_category__maincategory").filter(
            item_category__maincategory__user_id=request.user)
        context["items"] = all_items.exclude(item_category__maincategory__id=lug_cat.id)
        context["avail_luggage"] = all_items.filter(item_category__maincategory__id=lug_cat.id)

        context["mission_luggage"] = MissionItem.objects.all().filter(mission_id = mission.id).filter(storage=None)
        context["mission_items"] = MissionItem.objects.all().filter(mission_id = mission.id).exclude(storage=None)

    return render(request, "gearapp/mission_view.html", context)


class ItemAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') # Replace 'home' with the name of your home page URL
        else:
            return render(request, 'gearapp/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'gearapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login.html') # Replace 'login' with the name of your login page URL

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'gearapp/signup.html'