from django.urls import path
from . import views

app_name = 'constructor'

urlpatterns = [
    path('', views.constructor_view, name='constructor'),
    path('create-order/', views.create_constructor_order, name='create_order'),
    path('get-orders/', views.get_user_orders, name='get_orders'),
    
]