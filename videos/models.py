from django.db import models
from users.models import User

class Video(models.Model):

    titulo = models.CharField(max_length=200)

    descricao = models.TextField()

    url_youtube = models.URLField()

    categoria = models.CharField(max_length=100)
    
    
    preco = models.DecimalField(
    max_digits=8,
    decimal_places=2,
    default=0
)

    gratuito = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class CompraVideo(models.Model):

    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE
    )

    comprado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'aluno',
            'video'
        )   