from django.test import TestCase
from django.urls import reverse

from .forms import PedidoForm
from .models import Categoria, Juego, Pedido


class PedidoFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre="Pruebas")
        cls.juego = Juego.objects.create(
            categoria=cls.categoria,
            nombre="Juego de prueba",
            descripcion="Descripción de prueba.",
            imagen="juegos/prueba.png",
            precio=10000,
            cantidad_jugadores=4,
            edad_minima=8,
            stock=3,
            disponible=True,
        )
        cls.juego_agotado = Juego.objects.create(
            categoria=cls.categoria,
            nombre="Juego agotado",
            descripcion="Sin stock.",
            imagen="juegos/agotado.png",
            precio=8000,
            cantidad_jugadores=2,
            edad_minima=6,
            stock=0,
            disponible=True,
        )
        cls.juego_no_disponible = Juego.objects.create(
            categoria=cls.categoria,
            nombre="Juego no disponible",
            descripcion="No visible.",
            imagen="juegos/no-disponible.png",
            precio=9000,
            cantidad_jugadores=2,
            edad_minima=6,
            stock=2,
            disponible=False,
        )

    def datos_formulario(self, cantidad=1):
        return {
            "nombre_cliente": "Ana Pérez",
            "correo": "ANA@EJEMPLO.COM",
            "telefono": "+56 9 1234 5678",
            "cantidad": cantidad,
        }

    def test_formulario_acepta_datos_validos_y_normaliza(self):
        formulario = PedidoForm(data=self.datos_formulario())
        self.assertTrue(formulario.is_valid())
        self.assertEqual(formulario.cleaned_data["correo"], "ana@ejemplo.com")

    def test_formulario_solo_expone_campos_del_cliente(self):
        self.assertEqual(
            list(PedidoForm().fields),
            ["nombre_cliente", "correo", "telefono", "cantidad"],
        )

    def test_formulario_rechaza_cantidad_cero(self):
        self.assertFalse(PedidoForm(data=self.datos_formulario(0)).is_valid())

    def test_formulario_rechaza_cantidad_seis(self):
        self.assertFalse(PedidoForm(data=self.datos_formulario(6)).is_valid())

    def test_formulario_rechaza_correo_invalido(self):
        datos = self.datos_formulario()
        datos["correo"] = "correo-invalido"
        self.assertFalse(PedidoForm(data=datos).is_valid())

    def test_formulario_rechaza_telefono_con_letras(self):
        datos = self.datos_formulario()
        datos["telefono"] = "5691234ABC"
        self.assertFalse(PedidoForm(data=datos).is_valid())

    def test_get_formulario_para_juego_disponible(self):
        respuesta = self.client.get(
            reverse("catalogo:crear_pedido", args=[self.juego.id])
        )
        self.assertEqual(respuesta.status_code, 200)

    def test_juego_agotado_devuelve_404(self):
        respuesta = self.client.get(
            reverse("catalogo:crear_pedido", args=[self.juego_agotado.id])
        )
        self.assertEqual(respuesta.status_code, 404)

    def test_juego_no_disponible_devuelve_404(self):
        respuesta = self.client.get(
            reverse("catalogo:crear_pedido", args=[self.juego_no_disponible.id])
        )
        self.assertEqual(respuesta.status_code, 404)

    def test_pedido_valido_crea_pedido_descuenta_stock_y_redirige(self):
        respuesta = self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(2),
        )
        pedido = Pedido.objects.get()
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.url, reverse(
            "catalogo:comprobante_pedido", args=[pedido.codigo]
        ))
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(Juego.objects.get(id=self.juego.id).stock, 1)
        self.assertTrue(pedido.codigo.startswith("PED-"))
        self.assertLessEqual(len(pedido.codigo), 12)

    def test_no_permite_pedir_mas_que_el_stock(self):
        respuesta = self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(4),
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Pedido.objects.count(), 0)
        self.assertEqual(Juego.objects.get(id=self.juego.id).stock, 3)
        self.assertContains(respuesta, "No hay suficiente stock")

    def test_stock_insuficiente_no_crea_pedido_ni_modifica_stock(self):
        respuesta = self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(5),
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Pedido.objects.count(), 0)
        self.assertEqual(Juego.objects.get(id=self.juego.id).stock, 3)

    def test_post_valido_redirige_al_comprobante(self):
        respuesta = self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(),
        )
        pedido = Pedido.objects.get()
        self.assertRedirects(
            respuesta,
            reverse("catalogo:comprobante_pedido", args=[pedido.codigo]),
        )

    def test_codigo_es_unico(self):
        for nombre in ("Ana Pérez", "Luis Soto"):
            datos = self.datos_formulario()
            datos["nombre_cliente"] = nombre
            self.client.post(
                reverse("catalogo:crear_pedido", args=[self.juego.id]),
                datos,
            )
        codigos = list(Pedido.objects.values_list("codigo", flat=True))
        self.assertEqual(len(codigos), 2)
        self.assertEqual(len(set(codigos)), 2)
        self.assertTrue(all(len(codigo) <= 12 for codigo in codigos))

    def test_comprobante_responde_200(self):
        self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(),
        )
        codigo = Pedido.objects.get().codigo
        respuesta = self.client.get(
            reverse("catalogo:comprobante_pedido", args=[codigo])
        )
        self.assertEqual(respuesta.status_code, 200)

    def test_comprobante_y_recarga_no_duplican_pedido_ni_stock(self):
        respuesta = self.client.post(
            reverse("catalogo:crear_pedido", args=[self.juego.id]),
            self.datos_formulario(),
        )
        codigo = Pedido.objects.get().codigo
        url_comprobante = reverse("catalogo:comprobante_pedido", args=[codigo])
        self.assertEqual(respuesta.url, url_comprobante)
        self.assertEqual(self.client.get(url_comprobante).status_code, 200)
        self.assertEqual(self.client.get(url_comprobante).status_code, 200)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(Juego.objects.get(id=self.juego.id).stock, 2)

    def test_codigo_inexistente_devuelve_404(self):
        respuesta = self.client.get(
            reverse("catalogo:comprobante_pedido", args=["PED-XXXXXXXX"])
        )
        self.assertEqual(respuesta.status_code, 404)
