from decimal import Decimal
import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.


# ==========================================================
# MODELO RULETA
# ==========================================================
class Ruleta(models.Model):

    partida = models.OneToOneField(
        "appcom.Partida",
        on_delete=models.CASCADE,
        related_name="ruleta",
    )

    numero_resultado = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Ruleta - Partida {self.partida_id}"


class NumeroRuleta(models.Model):

    num = models.PositiveSmallIntegerField(unique=True)
    color = models.CharField(max_length=10)
    par = models.BooleanField()

    s12 = models.PositiveSmallIntegerField()
    fila = models.PositiveSmallIntegerField()
    colum = models.PositiveSmallIntegerField()
    medio = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.num} - {self.color}"


# ==========================================================
# MODELO PREMIO
# ==========================================================

class Premio(models.Model):
    TIPOS_APUESTA = [
        # APUESTAS INTERNAS
        ("pleno", "Número individual"),
        ("caballo", "Caballo (2 números)"),
        ("transversal", "Transversal (3 números)"),
        ("cuadro", "Cuadro (4 números)"),
        ("seisena", "Seisena (6 números)"),
        # APUESTAS EXTERNAS
        ("color", "Rojo / Negro"),
        ("paridad", "Par / Impar"),
        ("mitad", "Falta / Pasa"),
        ("docena", "Docenas"),
        ("columna", "Columnas"),
    ]

    MULTIPLICADORES = {
        "pleno": 35,
        "caballo": 17,
        "transversal": 11,
        "cuadro": 8,
        "seisena": 5,
        "color": 1,
        "paridad": 1,
        "mitad": 1,
        "docena": 2,
        "columna": 2,
    }

    ruleta = models.ForeignKey(
        Ruleta,
        on_delete=models.CASCADE,
        related_name="premios",
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_APUESTA)
    seleccion = models.CharField(max_length=30)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    ganada = models.BooleanField(null=True, blank=True, default=None)
    premio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

  