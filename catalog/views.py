from django.shortcuts import render
from .models import Product, Category


def catalog(request):
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
    print(f"View catalog вызвана")
    print(f"Товаров в queryset: {products.count()}")
    print(f"Категорий: {categories.count()}")
    print("=" * 50)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort,
    }
    return render(request, 'www/about.html', context)
