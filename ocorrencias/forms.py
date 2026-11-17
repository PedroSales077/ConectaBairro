from django import forms
from .models import Ocorrencia


class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ("descricao", "endereco_local", "foto", "latitude", "longitude")
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4, "maxlength": 1500}),
            "endereco_local": forms.TextInput(attrs={"maxlength": 220}),
            "latitude": forms.NumberInput(attrs={"step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"step": "0.000001"}),
        }
        help_texts = {
            "foto": "Envie uma imagem de até 5 MB. Formatos aceitos conforme validação de imagem.",
            "latitude": "Opcional. Informe coordenadas decimais, se souber.",
            "longitude": "Opcional. Informe coordenadas decimais, se souber.",
        }

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")
        if foto and foto.size > 5 * 1024 * 1024:
            raise forms.ValidationError("A imagem deve ter no máximo 5 MB.")
        return foto

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        if (latitude is None) != (longitude is None):
            raise forms.ValidationError(
                "Informe latitude e longitude juntas ou deixe ambas em branco."
            )
        if latitude is not None and not (-90 <= latitude <= 90):
            self.add_error("latitude", "A latitude deve estar entre -90 e 90.")
        if longitude is not None and not (-180 <= longitude <= 180):
            self.add_error("longitude", "A longitude deve estar entre -180 e 180.")
        return cleaned_data
