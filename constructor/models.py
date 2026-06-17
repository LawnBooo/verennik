from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ConstructorOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]
    
    ORDER_TYPES = [
        ('constructor', 'Заказ из конструктора'),
        ('custom', 'Индивидуальный заказ'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='constructor_orders', null=True, blank=True)

    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    
    product_type = models.CharField('Тип изделия', max_length=50, default='ФУТБОЛКА')
    color = models.CharField('Цвет', max_length=20, default='#ffffff')
    size = models.CharField('Размер', max_length=20, blank=True, null=True)
    side = models.CharField('Сторона', max_length=10, default='front')
    customization_type = models.CharField('Тип кастомизации', max_length=50, blank=True, null=True)
    
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    order_type = models.CharField('Тип заказа', max_length=20, choices=ORDER_TYPES, default='constructor')
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    design_image = models.ImageField('Изображение дизайна', upload_to='constructor_designs/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Заказ из конструктора'
        verbose_name_plural = 'Заказы из конструктора'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ #{self.id} - {self.name} ({self.product_type})'
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def get_order_type_display(self):
        return dict(self.ORDER_TYPES).get(self.order_type, self.order_type)

    def save(self, *args, **kwargs):

        if not self.user_id and hasattr(self, '_request') and self._request.user.is_authenticated:
            self.user = self._request.user
        super().save(*args, **kwargs)