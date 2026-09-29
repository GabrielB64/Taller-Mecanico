from django import forms
from django.contrib.auth.models import User

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


class EmpleadoForm(forms.ModelForm):

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        required=True
    )

    password_temporal = forms.CharField(
        label="Contraseña temporal",
        widget=forms.PasswordInput,
        min_length=8,
        required=True
    )

    class Meta:
        model = Empleado
        fields = [
            "nombre",
            "apellido",
            "rut",
            "telefono",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nombre de usuario ya está registrado."
            )

        return username

    def save(self, commit=True):
        empleado = super().save(commit=False)

        username = self.cleaned_data["username"]
        password = self.cleaned_data["password_temporal"]

        usuario = User.objects.create_user(
            username=username,
            password=password
        )

        usuario.is_staff = False
        usuario.is_superuser = False
        usuario.save()

        empleado.usuario = usuario
        empleado.password_change_required = True

        if commit:
            empleado.save()

        return empleado
    
class EmpleadoEditarForm(forms.ModelForm):

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