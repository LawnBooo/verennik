from django.contrib import admin
from django.contrib.admin import AdminSite

class VerennikAdminSite(AdminSite):
    site_header = "VERENNIK Администрация"
    site_title = "VERENNIK"
    index_title = "Панель управления"