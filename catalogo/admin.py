from django.contrib import admin

from .models import Categoria, Juego, Pedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "categoria",
        "precio",
        "cantidad_jugadores",
        "edad_minima",
        "stock",
        "disponible",
    )
    list_filter = ("categoria", "disponible")
    search_fields = ("nombre", "descripcion", "categoria__nombre")
    ordering = ("nombre",)
    list_editable = ("stock", "disponible")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre_cliente",
        "juego",
        "cantidad",
        "correo",
        "telefono",
        "fecha_hora",
    )
    list_filter = ("fecha_hora", "juego")
    search_fields = (
        "codigo",
        "nombre_cliente",
        "correo",
        "telefono",
        "juego__nombre",
    )
    ordering = ("-fecha_hora",)
    readonly_fields = ("fecha_hora",)


admin.site.site_header = "Administración Tienda de Juegos"
admin.site.site_title = "Tienda de Juegos"
admin.site.index_title = "Gestión de catálogo y pedidos"
