from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from .models import (
    Empleado,
    Herramienta,
    Repuestos,
    Trabajo,
)

from .forms import (
    EmpleadoForm,
    EmpleadoEditarForm,
    HerramientaForm,
    RepuestoForm,
    TrabajoForm,
)

def inicio(request):
    return render(request, "inicio.html")
# ============================================================
# PERMISOS
# ============================================================

def es_admin(user):
    return user.is_authenticated and user.is_staff


# ============================================================
# DASHBOARDS
# ============================================================

@login_required
def empleado_dashboard(request):

    trabajos_pendientes = Trabajo.objects.filter(
        estado__in=["Pendiente", "En progreso"]
    ).count()

    total_repuestos = Repuestos.objects.count()

    total_herramientas = Herramienta.objects.count()

    return render(
        request,
        "dashboard/empleado.html",
        {
            "trabajos_pendientes": trabajos_pendientes,
            "total_repuestos": total_repuestos,
            "total_herramientas": total_herramientas,
        }
    )


@login_required
@user_passes_test(es_admin)
def admin_dashboard(request):

    total_empleados = Empleado.objects.count()
    total_herramientas = Herramienta.objects.count()
    total_repuestos = Repuestos.objects.count()
    total_trabajos = Trabajo.objects.count()

    return render(
        request,
        "dashboard/admin.html",
        {
            "total_empleados": total_empleados,
            "total_herramientas": total_herramientas,
            "total_repuestos": total_repuestos,
            "total_trabajos": total_trabajos,
        }
    )


# ============================================================
# TRABAJOS
# ============================================================

@login_required
def trabajos_lista(request):

    trabajos = Trabajo.objects.all().order_by("-id")

    return render(
        request,
        "trabajos/lista.html",
        {
            "trabajos": trabajos
        }
    )


@login_required
def trabajo_detalle(request, pk):

    trabajo = get_object_or_404(
        Trabajo,
        pk=pk
    )

    return render(
        request,
        "trabajos/detalle.html",
        {
            "trabajo": trabajo
        }
    )


@login_required
def trabajo_crear(request):

    if request.method == "POST":

        form = TrabajoForm(request.POST)

        if form.is_valid():

            trabajo = form.save()

            messages.success(
                request,
                f"Trabajo #{trabajo.id} creado correctamente."
            )

            return redirect(
                "trabajo_detalle",
                pk=trabajo.pk
            )

    else:

        form = TrabajoForm()

    return render(
        request,
        "trabajos/formulario.html",
        {
            "form": form
        }
    )


@login_required
def trabajo_editar(request, pk):

    trabajo = get_object_or_404(
        Trabajo,
        pk=pk
    )

    if request.method == "POST":

        form = TrabajoForm(
            request.POST,
            instance=trabajo
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"Trabajo #{trabajo.id} actualizado correctamente."
            )

            return redirect(
                "trabajo_detalle",
                pk=trabajo.pk
            )

    else:

        form = TrabajoForm(
            instance=trabajo
        )

    return render(
        request,
        "trabajos/formulario.html",
        {
            "form": form,
            "trabajo": trabajo
        }
    )


# ============================================================
# EMPLEADOS
# ============================================================

@login_required
@user_passes_test(es_admin)
def empleados_lista(request):

    empleados = Empleado.objects.all().order_by(
        "apellido",
        "nombre"
    )

    return render(
        request,
        "empleados/lista.html",
        {
            "empleados": empleados
        }
    )


@login_required
@user_passes_test(es_admin)
def empleado_crear(request):

    if request.method == "POST":
        form = EmpleadoForm(request.POST)

        if form.is_valid():
            empleado = form.save()

            messages.success(
                request,
                f"Empleado {empleado.nombre} {empleado.apellido} creado correctamente."
            )

            return redirect("empleados_lista")

    else:
        form = EmpleadoForm()

    return render(
        request,
        "empleados/formulario.html",
        {
            "form": form,
            "titulo": "Crear empleado",
        }
    )


@login_required
@user_passes_test(es_admin)
def empleado_editar(request, pk):

    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == "POST":
        form = EmpleadoEditarForm(
            request.POST,
            instance=empleado
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Empleado actualizado correctamente."
            )

            return redirect("empleados_lista")

    else:
        form = EmpleadoEditarForm(instance=empleado)

    return render(
        request,
        "empleados/formulario.html",
        {
            "form": form,
            "empleado": empleado,
            "titulo": "Editar empleado",
        }
    )
    
@login_required
def cambiar_password(request):

    empleado = getattr(request.user, "empleado", None)

    if empleado is None:
        return redirect("inicio")

    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            usuario = form.save()

            # Evita que Django cierre la sesión después del cambio
            update_session_auth_hash(request, usuario)

            empleado.password_change_required = False
            empleado.save(update_fields=["password_change_required"])

            messages.success(
                request,
                "Tu contraseña fue cambiada correctamente."
            )

            return redirect("empleado_dashboard")

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "cambiar_password.html",
        {
            "form": form,
        }
    )


@login_required
@user_passes_test(es_admin)
def empleado_eliminar(request, pk):

    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == "POST":

        usuario = empleado.usuario

        with transaction.atomic():
            empleado.delete()
            usuario.delete()

        messages.success(
            request,
            f"El empleado {empleado.nombre} {empleado.apellido} fue eliminado correctamente."
        )

        return redirect("empleados_lista")

    return render(
        request,
        "eliminar.html",
        {
            "object": empleado,
            "cancel_url": reverse("empleados_lista"),
        }
    )


# ============================================================
# HERRAMIENTAS
# ============================================================

@login_required
def herramientas_lista(request):

    herramientas = Herramienta.objects.all().order_by(
        "nombre"
    )

    return render(
        request,
        "herramientas/lista.html",
        {
            "herramientas": herramientas
        }
    )


@login_required
def herramienta_editar(request, pk):

    herramienta = get_object_or_404(
        Herramienta,
        pk=pk
    )

    if request.method == "POST":

        form = HerramientaForm(
            request.POST,
            instance=herramienta
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"Herramienta '{herramienta.nombre}' actualizada correctamente."
            )

            return redirect("herramientas_lista")

    else:

        form = HerramientaForm(
            instance=herramienta
        )

    return render(
        request,
        "herramientas/formulario.html",
        {
            "form": form,
            "herramienta": herramienta
        }
    )


@login_required
@user_passes_test(es_admin)
def herramienta_crear(request):

    if request.method == "POST":

        form = HerramientaForm(request.POST)

        if form.is_valid():

            herramienta = form.save()

            messages.success(
                request,
                f"Herramienta '{herramienta.nombre}' creada correctamente."
            )

            return redirect("herramientas_lista")

    else:

        form = HerramientaForm()

    return render(
        request,
        "herramientas/formulario.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(es_admin)
def herramienta_eliminar(request, pk):

    herramienta = get_object_or_404(
        Herramienta,
        pk=pk
    )

    if request.method == "POST":

        nombre = herramienta.nombre

        herramienta.delete()

        messages.success(
            request,
            f"Herramienta '{nombre}' eliminada correctamente."
        )

        return redirect("herramientas_lista")

    return render(
        request,
        "eliminar.html",
        {
            "object": herramienta,
            "cancel_url": reverse("herramientas_lista"),
        }
    )


# ============================================================
# REPUESTOS
# ============================================================

@login_required
def repuestos_lista(request):

    repuestos = Repuestos.objects.all().order_by(
        "nombre"
    )

    return render(
        request,
        "repuestos/lista.html",
        {
            "repuestos": repuestos
        }
    )


@login_required
def repuesto_editar(request, pk):

    repuesto = get_object_or_404(
        Repuestos,
        pk=pk
    )

    if request.method == "POST":

        form = RepuestoForm(
            request.POST,
            instance=repuesto
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"Repuesto '{repuesto.nombre}' actualizado correctamente."
            )

            return redirect("repuestos_lista")

    else:

        form = RepuestoForm(
            instance=repuesto
        )

    return render(
        request,
        "repuestos/formulario.html",
        {
            "form": form,
            "repuesto": repuesto
        }
    )


@login_required
@user_passes_test(es_admin)
def repuesto_crear(request):

    if request.method == "POST":

        form = RepuestoForm(request.POST)

        if form.is_valid():

            repuesto = form.save()

            messages.success(
                request,
                f"Repuesto '{repuesto.nombre}' creado correctamente."
            )

            return redirect("repuestos_lista")

    else:

        form = RepuestoForm()

    return render(
        request,
        "repuestos/formulario.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(es_admin)
def repuesto_eliminar(request, pk):

    repuesto = get_object_or_404(
        Repuestos,
        pk=pk
    )

    if request.method == "POST":

        nombre = repuesto.nombre

        repuesto.delete()

        messages.success(
            request,
            f"Repuesto '{nombre}' eliminado correctamente."
        )

        return redirect("repuestos_lista")

    return render(
        request,
        "eliminar.html",
        {
            "object": repuesto,
            "cancel_url": reverse("repuestos_lista"),
        }
    )


def login_admin(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(request, "Credenciales incorrectas o el usuario no es administrador.")

    return render(request, "login.html", {
        "tipo": "Administrador",
        "tipo_login": "admin",
    })


def login_empleado(request):

    if request.user.is_authenticated:

        if hasattr(request.user, "empleado"):
            empleado = request.user.empleado

            if empleado.password_change_required:
                return redirect("cambiar_password")

            return redirect("empleado_dashboard")

        return redirect("inicio")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and hasattr(user, "empleado"):

            login(request, user)

            empleado = user.empleado

            if empleado.password_change_required:
                return redirect("cambiar_password")

            return redirect("empleado_dashboard")

        messages.error(
            request,
            "Credenciales incorrectas o el usuario no es un empleado."
        )

    return render(
        request,
        "login.html",
        {
            "tipo": "Empleado",
            "tipo_login": "empleado",
        }
    )