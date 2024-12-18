"""
URL configuration for gearstorage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gearapp.views import items_list, current_storage, usual_storage, ItemAPIView, login_view, logout_view, SignUpView, missions_list, mission_create_view, mission_view, mission_print_out
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', items_list),
    path('current_storage.html', current_storage),
    path('usual_storage.html', usual_storage),
    path('missions_list.html', missions_list),
    path('mission_create_view.html', mission_create_view),
    path('mission_view.html/<str:id>', mission_view),
    path('mission_print_out.html/<str:id>', mission_print_out),
    path('api/itemlist/',ItemAPIView.as_view()),
    path('login.html', login_view, name='login'),
    path('logout.html', logout_view, name='logout'),
    path('signup.html', SignUpView.as_view(), name='signup')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
