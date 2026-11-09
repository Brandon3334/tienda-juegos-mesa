from django.urls import path

from . import views


app_name = "catalogo"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("juego/<int:juego_id>/", views.detalle_juego, name="detalle_juego"),
    path("juego/<int:juego_id>/pedido/", views.crear_pedido, name="crear_pedido"),
    path(
        "pedido/<str:codigo>/comprobante/",
        views.comprobante_pedido,
        name="comprobante_pedido",
    ),
]
