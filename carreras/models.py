from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Carrera(models.Model):
    class Tipo(models.TextChoices):
        GALGOS = "galgos", "Galgos"
        CABALLOS = "caballos", "Caballos"
        COCHES = "coches", "Coches"

    class Estado(models.TextChoices):
        ABIERTA = "abierta", "Abierta para apuestas"
        CERRADA = "cerrada", "Apuestas cerradas"
        LIQUIDADA = "liquidada", "Liquidada"

    partida = models.OneToOneField(
        "appcom.Partida",
        on_delete=models.PROTECT,
        related_name="carrera",
    )
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ABIERTA,
    )


class PremioPorPuesto(models.Model):
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        related_name="premios",
    )
    puesto = models.PositiveSmallIntegerField(
        choices=[(1, "Primero"), (2, "Segundo"), (3, "Tercero")],
    )
    multiplicador = models.DecimalField(max_digits=8, decimal_places=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["carrera", "puesto"],
                name="carreras_premio_unico_por_puesto",
            ),
            models.CheckConstraint(
                condition=models.Q(puesto__in=[1, 2, 3]),
                name="carreras_puesto_premiado_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(multiplicador__gt=0),
                name="carreras_multiplicador_positivo",
            ),
        ]


class Apuesta(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="apuestas_carreras",
    )

    importe = models.DecimalField(max_digits=12, decimal_places=2)
    importe_abonado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(importe__gt=0),
                name="carreras_apuesta_importe_positivo",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(importe_abonado__isnull=True)
                    | models.Q(importe_abonado__gte=0)
                ),
                name="carreras_abono_no_negativo",
            ),
        ]
