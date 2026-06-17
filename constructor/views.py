from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import base64
import uuid
from django.core.files.base import ContentFile
from .models import ConstructorOrder

def constructor_view(request):
    """Страница конструктора"""
    return render(request, 'constructor/constructor.html')

@csrf_exempt
@require_POST
def create_constructor_order(request):
    """
    Создание заказа из конструктора
    """
    try:
        # Парсим JSON из тела запроса
        data = json.loads(request.body)
        
        # Извлекаем данные из формы
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        comment = data.get('comment', '').strip()
        
        # Валидация обязательных полей
        if not name or not phone:
            return JsonResponse({
                'status': 'error',
                'message': 'Пожалуйста, заполните имя и телефон'
            }, status=400)
        
        # Получаем информацию о дизайне
        design_info = data.get('design_info', {})
        product_type = design_info.get('product', 'ФУТБОЛКА')
        color = design_info.get('color', '#ffffff')
        size = design_info.get('size', 'Не выбран')
        side = design_info.get('side', 'front')
        customization_type = design_info.get('customization_type', 'classic')
        
        # Создаем заказ в базе данных
        order = ConstructorOrder.objects.create(
            name=name,
            phone=phone,
            email=email,
            comment=comment,
            product_type=product_type,
            color=color,
            size=size,
            side=side,
            customization_type=customization_type,
            status='pending',
            order_type='constructor'
        )
        
        # Если пользователь авторизован, привязываем заказ к нему
        if request.user.is_authenticated:
            order.user = request.user
            order.save()
        
        # Если есть изображение дизайна (base64), сохраняем его
        if data.get('design_image'):
            try:
                image_data = data['design_image']
                # Проверяем, что это base64 изображение
                if ';base64,' in image_data:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    filename = f"design_{order.id}_{uuid.uuid4().hex[:8]}.{ext}"
                    order.design_image.save(filename, ContentFile(base64.b64decode(imgstr)), save=True)
            except Exception as e:
                print(f"Ошибка сохранения изображения: {e}")
        
        # Отправляем письмо-уведомление
        try:
            subject = f'Новый заказ из конструктора #{order.id}'
            email_message = f'''
Новый заказ из конструктора!

Номер заказа: {order.id}
Имя: {name}
Телефон: {phone}
Email: {email or 'Не указан'}

Детали заказа:
- Тип изделия: {product_type}
- Цвет: {color}
- Размер: {size}
- Сторона: {side}
- Тип кастомизации: {customization_type}

Комментарий: {comment or 'Нет комментария'}

Ссылка в админке: /admin/constructor/constructororder/{order.id}/change/
'''
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['lordlizo@yandex.ru'],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Заказ успешно создан! Мы свяжемся с вами в ближайшее время.',
            'order_id': order.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при создании заказа: {str(e)}'
        }, status=500)

@login_required
def get_user_orders(request):
    """API для получения заказов пользователя (для AJAX)"""
    orders = ConstructorOrder.objects.filter(user=request.user).order_by('-created_at')
    
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'name': order.name,
            'phone': order.phone,
            'email': order.email,
            'comment': order.comment,
            'product_type': order.product_type,
            'color': order.color,
            'size': order.size,
            'side': order.side,
            'customization_type': order.customization_type,
            'status': order.status,
            'status_display': order.get_status_display(),
            'order_type_display': order.get_order_type_display(),
            'created_at': order.created_at.strftime('%d.%m.%Y %H:%M'),
            'design_image': order.design_image.url if order.design_image else None
        })
    
    return JsonResponse({
        'status': 'success',
        'orders': orders_data
    })