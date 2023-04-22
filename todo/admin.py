from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class QuoteAdmin(admin.ModelAdmin):
    pass
