from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from www.admin import VerennikAdminSite

admin_site = VerennikAdminSite(name='verennik_admin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('www.urls')),
    path('about/', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('orders/', include('orders.urls')),
    path('constructor/', include('constructor.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)