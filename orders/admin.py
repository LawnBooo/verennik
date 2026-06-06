from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'order_type', 'status', 'created_at')
    list_filter = ('status', 'order_type', 'created_at')
    search_fields = ('id', 'name', 'phone', 'email', 'description')
    ordering = ('-created_at',)
    list_editable = ('status',)