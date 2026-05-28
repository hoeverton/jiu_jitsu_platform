from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    TIPOS = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('preparador', 'Preparador'),
        ('nutricionista', 'Nutricionista'),
        ('recovery', 'Recovery'),
    )

    tipo_usuario = models.CharField(max_length=20, choices=TIPOS)
