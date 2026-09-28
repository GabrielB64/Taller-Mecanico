from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from .models import Trabajo
from .forms import TrabajoForm


@login_required
def trabajos_lista(request):

    trabajos = Trabajo.objects.all()

    return render(
        request,
        'trabajos/lista.html',
        {
            'trabajos': trabajos
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
        'trabajos/detalle.html',
        {
            'trabajo': trabajo
        }
    )


@login_required
def trabajo_crear(request):

    if request.method == 'POST':

        form = TrabajoForm(request.POST)

        if form.is_valid():

            trabajo = form.save()

            return redirect(
                'trabajo_detalle',
                pk=trabajo.pk
            )

    else:

        form = TrabajoForm()

    return render(
        request,
        'trabajos/formulario.html',
        {
            'form': form
        }
    )


@login_required
def trabajo_editar(request, pk):

    trabajo = get_object_or_404(
        Trabajo,
        pk=pk
    )

    if request.method == 'POST':

        form = TrabajoForm(
            request.POST,
            instance=trabajo
        )

        if form.is_valid():

            form.save()

            return redirect(
                'trabajo_detalle',
                pk=trabajo.pk
            )

    else:

        form = TrabajoForm(
            instance=trabajo
        )

    return render(
        request,
        'trabajos/formulario.html',
        {
            'form': form,
            'trabajo': trabajo
        }
    )