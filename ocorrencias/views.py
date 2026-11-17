from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import OcorrenciaForm
from .models import Ocorrencia


def nova_ocorrencia(request):
    if request.method == "POST":
        form = OcorrenciaForm(request.POST, request.FILES)
        if form.is_valid():
            ocorrencia = form.save()
            return render(
                request,
                "ocorrencias/sucesso.html",
                {"ocorrencia": ocorrencia},
            )
    else:
        form = OcorrenciaForm()

    return render(request, "ocorrencias/nova.html", {"form": form})


@staff_member_required
def gestao_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all()
    return render(
        request,
        "ocorrencias/gestao.html",
        {"ocorrencias": ocorrencias, "status_choices": Ocorrencia.Status.choices},
    )


@staff_member_required
@require_POST
def atualizar_status(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    novo_status = request.POST.get("status")
    status_validos = {choice[0] for choice in Ocorrencia.Status.choices}

    if novo_status not in status_validos:
        messages.error(request, "Status inválido. Nenhuma alteração foi realizada.")
        return redirect("gestao_ocorrencias")

    ocorrencia.status = novo_status
    ocorrencia.save(update_fields=["status"])
    messages.success(request, f"Status da ocorrência #{ocorrencia.pk} atualizado.")
    return redirect("gestao_ocorrencias")
