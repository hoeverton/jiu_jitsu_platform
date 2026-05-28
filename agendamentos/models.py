from django.db import models
from users.models import User
from professores.models import Professor


class Disponibilidade(models.Model):

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='disponibilidades'
    )

    data = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    disponivel = models.BooleanField(default=True)

    def __str__(self):

        return f'{self.professor} - {self.data}'


class Agendamento(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    )

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE
    )

    disponibilidade = models.ForeignKey(
        Disponibilidade,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.aluno} - {self.professor}'