from django.db import models
from users.models import User


class Professor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    faixa = models.CharField(max_length=50)

    biografia = models.TextField()

    preco_hora = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    cidade = models.CharField(max_length=100)

    especialidade = models.CharField(max_length=100)

    foto = models.ImageField(
        upload_to='professores/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username