from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Categoria, Juego


def catalogo(request):
    consulta = request.GET.get("q", "").strip()
    categoria_seleccionada = request.GET.get("categoria", "").strip()

    juegos = Juego.objects.filter(disponible=True).select_related("categoria")
    if consulta:
        juegos = juegos.filter(
            Q(nombre__icontains=consulta) | Q(descripcion__icontains=consulta)
        )

    try:
        categoria_id = int(categoria_seleccionada)
    except (TypeError, ValueError):
        categoria_id = None

    if categoria_id is not None:
        juegos = juegos.filter(categoria_id=categoria_id)

    contexto = {
        "juegos": juegos.order_by("nombre"),
        "categorias": Categoria.objects.order_by("nombre"),
        "consulta": consulta,
        "categoria_seleccionada": categoria_seleccionada,
    }
    return render(request, "catalogo/catalogo.html", contexto)


def detalle_juego(request, juego_id):
    juego = get_object_or_404(
        Juego.objects.filter(disponible=True).select_related("categoria"),
        id=juego_id,
    )
    return render(request, "catalogo/detalle_juego.html", {"juego": juego})
