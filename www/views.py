from django.shortcuts import render
from catalog.models import Product, Category
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from constructor.models import ConstructorOrder
from django.contrib.auth.decorators import login_required

def index_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        # Валидация полей
        if not name or not phone:
            return JsonResponse(
                {'status': 'error', 'message': 'Пожалуйста, заполните обязательные поля (Имя и Телефон)'}, status=400)

        # Формируем тему и текст письма
        subject = f'Новая заявка/отзыв от {name}'
        email_message = f'Имя: {name}\nТелефон: {phone}\n\nСообщение:\n{message}'

        try:
            # Отправка письма
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['lordlizo@yandex.ru'],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Ваша заявка успешно отправлена!'})
        except Exception as e:
            # Превращаем ЛЮБУЮ ошибку в понятный текст для JS
            error_message = f"Ошибка SMTP: {type(e).__name__} - {str(e)}"
            return JsonResponse({'status': 'error', 'message': error_message},
                                status=200)  # Ставим статус 200, чтобы JS не уходил в .catch()

    return render(request, 'www/index.html')

def index(request):
    return render(request, 'www/index.html')

def about(request):
    """Страница каталога"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    sort = request.GET.get('sort')
    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    print("=" * 50)
    print(f"about view вызвана (каталог)")
    print(f"Товаров: {products.count()}")
    print("=" * 50)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort,
    }
    return render(request, 'www/about.html', context)

def achievements(request):
    return render(request, 'www/achievements.html')


def favorites(request):
    return render(request, 'www/favorites.html')

def new_life(request):
    return render(request, 'www/new_life.html')

@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    # Получаем заказы из конструктора
    orders = ConstructorOrder.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'www/profile.html', context)