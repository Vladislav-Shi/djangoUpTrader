from django.urls import path

from app.views import generate_menu

urlpatterns = [
    path('menu/', generate_menu, name='menu'),
]