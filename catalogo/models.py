from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="juegos",
        verbose_name="Categoría",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(verbose_name="Descripción")
    imagen = models.ImageField(upload_to="juegos/", verbose_name="Imagen de la caja")
    precio = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Precio",
    )
    cantidad_jugadores = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad de jugadores",
    )
    edad_minima = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Edad mínima",
    )
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    nombre_cliente = models.CharField(max_length=150, verbose_name="Nombre del cliente")
    correo = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    cantidad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora")
    codigo = models.CharField(max_length=12, unique=True)

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre_cliente}"
