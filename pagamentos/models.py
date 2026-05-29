from django.db import models
from agendamentos.models import Agendamento


class Pagamento(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('cancelado', 'Cancelado'),
    )

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    mercado_pago_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )