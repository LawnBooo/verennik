from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about, name='about'),
    path('achievements/', views.achievements, name='achievements'),
    path('favorites/', views.favorites, name='favorites'),
    path('new_life/', views.new_life, name='new_life'),
    path('profile/', views.profile_view, name='profile')
    
]