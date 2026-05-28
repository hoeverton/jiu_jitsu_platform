from django.db import models
from users.models import User
from professores.models import Professor
from agendamentos.models import Agendamento


class Avaliacao(models.Model):

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    comentario = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.professor} - {self.nota}'