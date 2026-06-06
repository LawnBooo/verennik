from django.db import models
from catalog.models import Product
from django.contrib.auth import models as auth_models

class Order(models.Model):
    """Заказ/Заявка"""
    ORDER_TYPES = [
        ('purchase', 'Покупка товара'),
        ('custom', 'Кастом одежды'),
        ('upcycle', 'Обновление старой одежды'),
    ]

    STATUSES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )

    order_type = models.CharField('Тип заявки', max_length=20, choices=ORDER_TYPES)
    status = models.CharField('Статус', max_length=20, choices=STATUSES, default='new')
    quantity = models.PositiveIntegerField('Количество', default=1)

    # Контакты
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Товар')
    description = models.TextField('Описание заказа', help_text='Опишите, что хотите заказать или изменить')
    image = models.ImageField('Фото', upload_to='orders/', blank=True, null=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_order_type_display()} - {self.name} - {self.created_at.strftime('%d.%m.%Y')}"