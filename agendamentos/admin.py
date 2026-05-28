from django.contrib import admin
from .models import (
    Disponibilidade,
    Agendamento
)

admin.site.register(Disponibilidade)
admin.site.register(Agendamento)