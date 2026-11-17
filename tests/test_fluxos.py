from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from ecopontos.models import Ecoponto
from ocorrencias.models import Ocorrencia


def imagem_teste():
    buffer = BytesIO()
    Image.new("RGB", (20, 20), color="green").save(buffer, format="JPEG")
    return SimpleUploadedFile(
        "teste.jpg", buffer.getvalue(), content_type="image/jpeg"
    )


class EcopontoTests(TestCase):
    def test_inicio_exibe_somente_ecopontos_ativos(self):
        Ecoponto.objects.create(
            nome="Ponto ativo",
            endereco="Rua de teste, 10",
            bairro="Vila Curuçá",
            horario_funcionamento="Segunda a sábado",
            materiais_aceitos="Entulho e recicláveis",
            ativo=True,
        )
        Ecoponto.objects.create(
            nome="Ponto inativo",
            endereco="Rua de teste, 20",
            bairro="Vila Curuçá",
            horario_funcionamento="Fechado",
            materiais_aceitos="Nenhum",
            ativo=False,
        )

        response = self.client.get(reverse("inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ponto ativo")
        self.assertNotContains(response, "Ponto inativo")


class OcorrenciaTests(TestCase):
    def test_registro_valido_cria_ocorrencia_pendente(self):
        response = self.client.post(
            reverse("nova_ocorrencia"),
            {
                "descricao": "Resíduos descartados na calçada.",
                "endereco_local": "Rua de teste, 100",
                "foto": imagem_teste(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ocorrencia.objects.count(), 1)
        ocorrencia = Ocorrencia.objects.first()
        self.assertEqual(ocorrencia.status, Ocorrencia.Status.PENDENTE)

    def test_foto_e_obrigatoria(self):
        response = self.client.post(
            reverse("nova_ocorrencia"),
            {
                "descricao": "Resíduos na via.",
                "endereco_local": "Rua de teste, 100",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ocorrencia.objects.count(), 0)
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_gestao_exige_usuario_staff(self):
        response = self.client.get(reverse("gestao_ocorrencias"))
        self.assertEqual(response.status_code, 302)

    def test_staff_pode_atualizar_status(self):
        usuario = get_user_model().objects.create_user(
            username="gestor", password="Senha-forte-123", is_staff=True
        )
        ocorrencia = Ocorrencia.objects.create(
            descricao="Descarte de resíduos.",
            endereco_local="Rua de teste, 100",
            foto=imagem_teste(),
        )
        self.client.force_login(usuario)

        response = self.client.post(
            reverse("atualizar_status", args=[ocorrencia.pk]),
            {"status": Ocorrencia.Status.ANALISADA},
        )

        self.assertRedirects(response, reverse("gestao_ocorrencias"))
        ocorrencia.refresh_from_db()
        self.assertEqual(ocorrencia.status, Ocorrencia.Status.ANALISADA)

    def test_status_invalido_nao_altera_registro(self):
        usuario = get_user_model().objects.create_user(
            username="gestor2", password="Senha-forte-123", is_staff=True
        )
        ocorrencia = Ocorrencia.objects.create(
            descricao="Descarte de resíduos.",
            endereco_local="Rua de teste, 100",
            foto=imagem_teste(),
        )
        self.client.force_login(usuario)

        self.client.post(
            reverse("atualizar_status", args=[ocorrencia.pk]),
            {"status": "status-inventado"},
        )

        ocorrencia.refresh_from_db()
        self.assertEqual(ocorrencia.status, Ocorrencia.Status.PENDENTE)
