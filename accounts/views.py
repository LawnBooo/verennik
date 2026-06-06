from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
from .models import Profile


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Регистрация успешно завершена!'})
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            return JsonResponse({'status': 'error', 'message': list(errors.values())[0]}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Вход выполнен успешно!'})
        return JsonResponse({'status': 'error', 'message': 'Неверное имя пользователя или пароль'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user

            # Обновляем username
            if 'username' in data and data['username']:
                user.username = data['username']

            # Обновляем email
            if 'email' in data and data['email']:
                user.email = data['email']

            # Обновляем телефон в профиле
            if 'phone' in data:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.phone = data['phone']
                profile.save()

            # Обновляем пароль
            if 'password' in data and data['password']:
                user.password = make_password(data['password'])
                user.save()
                update_session_auth_hash(request, user)
            else:
                user.save()

            return JsonResponse({'status': 'success', 'message': 'Профиль обновлен'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            avatar = request.FILES['avatar']

            # Проверка типа файла
            if not avatar.content_type.startswith('image/'):
                return JsonResponse({'status': 'error', 'message': 'Файл должен быть изображением'})

            # Проверка размера (макс 5MB)
            if avatar.size > 5 * 1024 * 1024:
                return JsonResponse({'status': 'error', 'message': 'Размер файла не должен превышать 5MB'})

            profile, created = Profile.objects.get_or_create(user=request.user)

            # Удаляем старый аватар
            if profile.avatar:
                if default_storage.exists(profile.avatar.path):
                    default_storage.delete(profile.avatar.path)

            # Сохраняем новый аватар
            profile.avatar = avatar
            profile.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Аватар обновлен',
                'avatar_url': profile.avatar.url
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Файл не загружен'}, status=400)


@login_required
def profile_view(request):
    user_orders = request.user.orders.all()
    return render(request, 'accounts/profile.html', {'orders': user_orders})