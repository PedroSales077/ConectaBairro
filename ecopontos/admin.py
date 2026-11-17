from django.contrib import admin
from .models import Ecoponto


@admin.register(Ecoponto)
class EcopontoAdmin(admin.ModelAdmin):
    list_display = ("nome", "bairro", "ativo")
    list_filter = ("ativo", "bairro")
    search_fields = ("nome", "endereco", "bairro")
