from django.db import models


class Ocorrencia(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ANALISADA = "analisada", "Analisada"
        ARQUIVADA = "arquivada", "Arquivada"

    descricao = models.TextField("descrição", max_length=1500)
    endereco_local = models.CharField("endereço do local", max_length=220)
    latitude = models.DecimalField(
        "latitude", max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        "longitude", max_digits=9, decimal_places=6, null=True, blank=True
    )
    foto = models.ImageField("fotografia", upload_to="ocorrencias/%Y/%m/")
    data_registro = models.DateTimeField("data do registro", auto_now_add=True)
    status = models.CharField(
        "status", max_length=12, choices=Status.choices, default=Status.PENDENTE
    )

    class Meta:
        ordering = ["-data_registro"]
        verbose_name = "ocorrência"
        verbose_name_plural = "ocorrências"

    def __str__(self):
        return f"Ocorrência #{self.pk} - {self.get_status_display()}"
