from django.urls import path
from gubookhub_app import views

app_name='rango'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
]