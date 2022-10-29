from django.contrib import admin
from .models import Article

# Mendaftarkan model Task pada admin panel
admin.site.register(Article)
