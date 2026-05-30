# favoritos/models.py
from django.db import models

from users.models import User
from professores.models import Professor


class Favorito(models.Model):

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'aluno',
            'professor'
        )

    def __str__(self):

        return f'{self.aluno} - {self.professor}'