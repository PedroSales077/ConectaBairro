from django.contrib import admin
from .models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "endereco_local", "data_registro", "status")
    list_filter = ("status", "data_registro")
    search_fields = ("descricao", "endereco_local")
    readonly_fields = ("data_registro",)
