from django.db import models


class Ecoponto(models.Model):
    nome = models.CharField("nome", max_length=120)
    endereco = models.CharField("endereço", max_length=200)
    bairro = models.CharField("bairro", max_length=100)
    horario_funcionamento = models.CharField("horário de funcionamento", max_length=160)
    materiais_aceitos = models.TextField("materiais aceitos")
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "ecoponto"
        verbose_name_plural = "ecopontos"

    def __str__(self):
        return self.nome
