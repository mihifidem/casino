# models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


# ==========================================================
# MODELO USER (NATIVO DE DJANGO)
# ==========================================================
# Se utiliza el modelo User nativo de Django.
# No es necesario definirlo nuevamente.
#
# Relaciones:
#
# User (1) -------- (1) ProfileUser
# User (1) -------- (*) Partida
#
# Un usuario tiene un perfil.
# Un usuario puede jugar múltiples partidas.
# ==========================================================


# ==========================================================
# MODELO PROFILEUSER
# ==========================================================

class ProfileUser(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True
    )

    direccion = models.CharField(
        max_length=255,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    saldo_virtual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("1000.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"


# ==========================================================
# MODELO PARTIDA
# ==========================================================

class Partida(models.Model):

    # Tipos de juegos disponibles en el casino virtual
    TIPOS_JUEGO = [
        ("blackjack", "Blackjack"),
        ("ruleta", "Ruleta"),
        ("slots", "Máquinas tragamonedas"),
        ("poker", "Póker"),
        ("dados", "Dados"),
        ("keno", "Keno"),
        ("carreras", "Carreras"),
        ("bingo", "Bingo"),
    ]

    # Resultados posibles
    RESULTADOS = [
        ("pendiente", "Pendiente"),
        ("victoria", "Victoria"),
        ("derrota", "Derrota"),
        ("empate", "Empate"),
    ]

    # Relación User (1) -> (*) Partida
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="partidas"
    )

    juego = models.CharField(
        max_length=20,
        choices=TIPOS_JUEGO
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    apuesta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    puntos = models.IntegerField(
        default=0
    )

    resultado = models.CharField(
        max_length=20,
        choices=RESULTADOS,
        default="pendiente"
    )

    premio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

    def __str__(self):
        return (
            f"Partida {self.pk} - "
            f"{self.usuario.username} - "
            f"{self.get_juego_display()}"
        )


# ==========================================================
# EJEMPLOS DE USO (EN VISTAS O EN DJANGO SHELL)
# ==========================================================
#
# from django.contrib.auth import get_user_model
# from decimal import Decimal
# from .models import ProfileUser, Partida
#
# User = get_user_model()
#
# # Crear usuario
# usuario = User.objects.create_user(
#     username="jugador1",
#     email="jugador1@example.com",
#     password="password_segura_123"
# )
#
# # Crear perfil asociado al usuario
# perfil = ProfileUser.objects.create(
#     user=usuario,
#     saldo_virtual=Decimal("1000.00")
# )
#
# # Crear una partida de Blackjack
# partida1 = Partida.objects.create(
#     usuario=usuario,
#     juego="blackjack",
#     apuesta=Decimal("50.00"),
#     puntos=21,
#     resultado="victoria",
#     premio=Decimal("100.00")
# )
#
# # Crear una partida de Ruleta
# partida2 = Partida.objects.create(
#     usuario=usuario,
#     juego="ruleta",
#     apuesta=Decimal("25.00"),
#     resultado="derrota",
#     premio=Decimal("0.00")
# )
#
# # Consultar el perfil de un usuario
# perfil = usuario.perfil
#
# # Consultar todas las partidas de un usuario
# partidas = usuario.partidas.all()
#
# # Consultar partidas de Blackjack
# partidas_blackjack = usuario.partidas.filter(
#     juego="blackjack"
# )
#
# ==========================================================
# COMANDOS PARA CREAR LAS MIGRACIONES
# ==========================================================
#
# pip install Pillow
#
# python manage.py makemigrations
# python manage.py migrate
#
# ==========================================================
# NOTAS
# ==========================================================
#
# 1. User es el modelo de autenticación nativo de Django.
#
# 2. ProfileUser utiliza OneToOneField:
#    Un usuario -> Un perfil.
#
# 3. Partida utiliza ForeignKey:
#    Un usuario -> Muchas partidas.
#
# 4. El campo "juego" permite almacenar partidas
#    de diferentes juegos del casino.
#
# 5. El saldo_virtual representa créditos ficticios.
#
# 6. La creación del perfil no es automática.
#    Puede implementarse mediante una señal post_save
#    o en el flujo de registro.
#
# 7. Las apuestas, premios y saldos deben actualizarse
#    mediante operaciones atómicas y transacciones
#    para evitar inconsistencias.
#
# 8. Este modelo está pensado para créditos virtuales
#    sin valor monetario ni posibilidad de retirada.
#
# ==========================================================