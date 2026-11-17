from django.urls import path
from . import views

urlpatterns = [
    path("ocorrencias/nova/", views.nova_ocorrencia, name="nova_ocorrencia"),
    path("gestao/", views.gestao_ocorrencias, name="gestao_ocorrencias"),
    path(
        "gestao/<int:pk>/status/",
        views.atualizar_status,
        name="atualizar_status",
    ),
]
