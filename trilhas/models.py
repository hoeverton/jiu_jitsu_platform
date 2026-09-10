from django.db import models

from users.models import User
from professores.models import Professor


class Trilha(models.Model):
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='trilhas',
        null=True,
        blank=True
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agendamentos_trilha'
        ordering = ['ordem', 'nome']
        constraints = [
            models.UniqueConstraint(
                fields=['professor', 'nome'],
                name='trilha_professor_nome_unico'
            )
        ]

    def __str__(self):
        return self.nome


class CategoriaTecnica(models.Model):
    trilha = models.ForeignKey(
        Trilha,
        on_delete=models.CASCADE,
        related_name='categorias'
    )
    nome = models.CharField(max_length=150)
    ordem = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agendamentos_categoriatecnica'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Tecnica(models.Model):
    trilha = models.ForeignKey(
        Trilha,
        on_delete=models.CASCADE,
        related_name='tecnicas'
    )
    categoria = models.ForeignKey(
        CategoriaTecnica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tecnicas'
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agendamentos_tecnica'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class ProgressoAluno(models.Model):
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progresso_tecnicas'
    )
    tecnica = models.ForeignKey(
        Tecnica,
        on_delete=models.CASCADE,
        related_name='progressos'
    )
    aprendido = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agendamentos_progressoaluno'
        constraints = [
            models.UniqueConstraint(
                fields=['aluno', 'tecnica'],
                name='progresso_aluno_tecnica_unico'
            )
        ]

    def __str__(self):
        return f'{self.aluno} - {self.tecnica}'


class TrilhaAluno(models.Model):
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='trilhas_alunos'
    )
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trilhas_aprendizado'
    )
    trilha = models.ForeignKey(
        Trilha,
        on_delete=models.CASCADE,
        related_name='alunos'
    )
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agendamentos_trilhaaluno'
        constraints = [
            models.UniqueConstraint(
                fields=['professor', 'aluno'],
                name='trilha_aluno_professor_unica'
            )
        ]

    def __str__(self):
        return f'{self.professor} - {self.aluno} - {self.trilha}'