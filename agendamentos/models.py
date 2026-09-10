from django.db import models
from users.models import User
from professores.models import Professor


class RegraDisponibilidade(models.Model):

    DIAS_SEMANA = (
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )

    DURACOES_AULA = (
        (30, '30 minutos'),
        (60, '60 minutos'),
        (90, '90 minutos'),
        (120, '120 minutos'),
    )

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='regras_disponibilidade'
    )

    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA
    )

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    duracao_aula = models.PositiveIntegerField(
        choices=DURACOES_AULA,
        default=60
    )

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            'dia_semana',
            'hora_inicio'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'professor',
                    'dia_semana',
                    'hora_inicio',
                    'hora_fim',
                ],
                name='regra_disponibilidade_unica'
            )
        ]

    def __str__(self):

        return (
            f'{self.professor} - '
            f'{self.get_dia_semana_display()} - '
            f'{self.hora_inicio} às {self.hora_fim}'
        )


class Disponibilidade(models.Model):

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='disponibilidades'
    )

    data = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    disponivel = models.BooleanField(
        default=True
    )

    regra = models.ForeignKey(
        RegraDisponibilidade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='horarios_gerados'
    )

    class Meta:

        ordering = [
            'data',
            'hora_inicio'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'professor',
                    'data',
                    'hora_inicio',
                    'hora_fim',
                ],
                name='disponibilidade_horario_unico'
            )
        ]

    def __str__(self):

        return (
            f'{self.professor} - '
            f'{self.data} - '
            f'{self.hora_inicio} às {self.hora_fim}'
        )


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
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            '-criado_em'
        ]

    def __str__(self):

        return (
            f'{self.aluno} - '
            f'{self.professor} - '
            f'{self.disponibilidade}'
        )
    








    