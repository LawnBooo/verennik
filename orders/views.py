from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from catalog.models import Product
from .models import Order
import json


def create_order_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = request.user if request.user.is_authenticated else None
            raw_title = data.get('product_title', '')
            order_type = 'purchase'
            if 'Услуга' in raw_title:
                order_type = 'custom'
            elif 'Обновление' in raw_title:
                order_type = 'upcycle'

            order = Order.objects.create(
                user=user,
                order_type=order_type,
                name=data.get('name'),
                phone=data.get('phone'),
                email=data.get('email', ''),
                description=f"Элемент: {raw_title}\nКомментарий: {data.get('comment', '')}"
            )

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests allowed'}, status=405)