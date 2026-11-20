from django.contrib import admin

# Register your models here.

from .models import Carrera, PremioPorPuesto, Apuesta

admin.site.register(Carrera)
admin.site.register(PremioPorPuesto)
admin.site.register(Apuesta)


