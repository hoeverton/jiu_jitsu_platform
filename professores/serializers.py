from rest_framework import serializers
from .models import Professor
from django.db.models import Avg
from agendamentos.models import Agendamento


class ProfessorSerializer(serializers.ModelSerializer):

    nome = serializers.CharField(
        source='user.username',
        read_only=True
    )

    media_avaliacoes = serializers.SerializerMethodField()

    total_avaliacoes = serializers.SerializerMethodField()

    total_aulas_concluidas = serializers.SerializerMethodField()

    total_alunos = serializers.SerializerMethodField()

    class Meta:

        model = Professor

        fields = [
            'id',
            'nome',
            'faixa',
            'biografia',
            'preco_hora',
            'cidade',
            'especialidade',
            'foto',
            'media_avaliacoes',
            'total_avaliacoes',
            'total_aulas_concluidas',
            'total_alunos',
        ]

    def get_media_avaliacoes(self, obj):

        media = obj.avaliacoes.aggregate(
            Avg('nota')
        )['nota__avg']

        if media is None:
            return 0

        return round(media, 1)

    def get_total_avaliacoes(self, obj):

        return obj.avaliacoes.count()
    
    def get_total_aulas_concluidas(self, obj):

        return Agendamento.objects.filter(
            professor=obj,
            status='concluido'
        ).count()


    def get_total_alunos(self, obj):

        return Agendamento.objects.filter(
            professor=obj,
            status='concluido'
        ).values(
            'aluno'
        ).distinct().count()
    
   