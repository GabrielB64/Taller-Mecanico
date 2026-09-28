from django import forms

from .models import (
    Empleado,
    Herramienta,
    Repuestos,
    Trabajo,
)


class BootstrapModelForm(forms.ModelForm):
    """
    ModelForm base que agrega automáticamente
    las clases de Bootstrap a los campos.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            else:
                field.widget.attrs["class"] = "form-control"


class EmpleadoForm(BootstrapModelForm):

    class Meta:
        model = Empleado

        fields = [
            "nombre",
            "apellido",
            "rut",
            "telefono",
        ]


class HerramientaForm(BootstrapModelForm):

    class Meta:
        model = Herramienta

        fields = [
            "nombre",
            "descripcion",
            "cantidad",
        ]


class RepuestoForm(BootstrapModelForm):

    class Meta:
        model = Repuestos

        fields = [
            "nombre",
            "descripcion",
            "cantidad",
        ]


class TrabajoForm(BootstrapModelForm):

    class Meta:
        model = Trabajo

        fields = [
            "estado",
            "criticidad",
            "descripcion",
            "hechos",
        ]

        widgets = {
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),

            "hechos": forms.Textarea(
                attrs={
                    "rows": 8,
                }
            ),
        }