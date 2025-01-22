from django.urls import path
from adotar import views

urlpatterns = [
    path('listar_pets/', views.listar_pets, name="listar_pets"),
]
