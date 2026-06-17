from django.contrib import admin
from .models import ConstructorOrder

@admin.register(ConstructorOrder)
class ConstructorOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'product_type', 'status', 'order_type', 'created_at']
    list_filter = ['status', 'product_type', 'customization_type', 'order_type', 'created_at']
    search_fields = ['name', 'phone', 'email', 'comment', 'id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Контактные данные', {
            'fields': ('user', 'name', 'phone', 'email', 'comment')
        }),
        ('Данные конструктора', {
            'fields': ('product_type', 'color', 'size', 'side', 'customization_type', 'design_image')
        }),
        ('Статус и тип', {
            'fields': ('status', 'order_type')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id and request.user.is_authenticated:
            obj.user = request.user
        super().save_model(request, obj, form, change)