from django.shortcuts import render
from .models import Ecoponto


def inicio(request):
    ecopontos = Ecoponto.objects.filter(ativo=True)
    return render(request, "ecopontos/inicio.html", {"ecopontos": ecopontos})
