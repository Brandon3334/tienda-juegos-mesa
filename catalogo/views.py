import secrets

from django.shortcuts import redirect, render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction

from .forms import PedidoForm
from .models import Categoria, Juego, Pedido


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


def _generar_codigo_pedido():
    caracteres = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        codigo = "PED-" + "".join(secrets.choice(caracteres) for _ in range(8))
        if not Pedido.objects.filter(codigo=codigo).exists():
            return codigo


def crear_pedido(request, juego_id):
    juego = get_object_or_404(
        Juego.objects.filter(disponible=True, stock__gt=0).select_related("categoria"),
        id=juego_id,
    )

    if request.method == "POST":
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            with transaction.atomic():
                juego_bloqueado = get_object_or_404(
                    Juego.objects.select_for_update().select_related("categoria"),
                    id=juego_id,
                    disponible=True,
                    stock__gt=0,
                )
                cantidad = formulario.cleaned_data["cantidad"]
                if cantidad > juego_bloqueado.stock:
                    formulario.add_error(
                        "cantidad",
                        "No hay suficiente stock para la cantidad solicitada.",
                    )
                else:
                    pedido = formulario.save(commit=False)
                    pedido.juego = juego_bloqueado
                    pedido.codigo = _generar_codigo_pedido()
                    pedido.save()
                    juego_bloqueado.stock -= cantidad
                    juego_bloqueado.save(update_fields=["stock"])
                    return redirect(
                        "catalogo:comprobante_pedido", codigo=pedido.codigo
                    )
    else:
        formulario = PedidoForm()

    return render(
        request,
        "catalogo/crear_pedido.html",
        {"formulario": formulario, "juego": juego},
    )


def comprobante_pedido(request, codigo):
    pedido = get_object_or_404(
        Pedido.objects.select_related("juego", "juego__categoria"),
        codigo=codigo,
    )
    total = pedido.juego.precio * pedido.cantidad
    return render(
        request,
        "catalogo/comprobante_pedido.html",
        {"pedido": pedido, "total": total},
    )
