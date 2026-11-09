import re

from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("nombre_cliente", "correo", "telefono", "cantidad")
        labels = {
            "nombre_cliente": "Nombre completo",
            "correo": "Correo electrónico",
            "telefono": "Teléfono",
            "cantidad": "Cantidad",
        }
        widgets = {
            "nombre_cliente": forms.TextInput(),
            "correo": forms.EmailInput(),
            "telefono": forms.TextInput(),
            "cantidad": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }

    def clean_nombre_cliente(self):
        nombre = self.cleaned_data["nombre_cliente"].strip()
        if len(nombre) < 2:
            raise forms.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )
        return nombre

    def clean_correo(self):
        return self.cleaned_data["correo"].strip().lower()

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        if not re.fullmatch(r"[0-9\s+\-()]+", telefono):
            raise forms.ValidationError("El teléfono contiene caracteres no válidos.")
        digitos = re.sub(r"\D", "", telefono)
        if not 8 <= len(digitos) <= 15:
            raise forms.ValidationError(
                "El teléfono debe contener entre 8 y 15 dígitos."
            )
        return telefono

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]
        if cantidad < 1:
            raise forms.ValidationError("La cantidad mínima es 1 unidad.")
        if cantidad > 5:
            raise forms.ValidationError("La cantidad máxima es 5 unidades.")
        return cantidad
