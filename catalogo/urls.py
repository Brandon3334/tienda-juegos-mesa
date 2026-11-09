from django.urls import path

from . import views


app_name = "catalogo"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("juego/<int:juego_id>/", views.detalle_juego, name="detalle_juego"),
]
