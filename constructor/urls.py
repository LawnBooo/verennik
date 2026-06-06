from django.urls import path
from . import views

urlpatterns = [
    path('', views.constructor_view, name='constructor'),
]