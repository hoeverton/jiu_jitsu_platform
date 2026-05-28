from rest_framework import serializers
from .models import Professor
from django.db.models import Avg


class ProfessorSerializer(serializers.ModelSerializer):

    media_avaliacoes = serializers.SerializerMethodField()

    total_avaliacoes = serializers.SerializerMethodField()

    class Meta:

        model = Professor

        fields = [
            'id',
            'faixa',
            'biografia',
            'preco_hora',
            'cidade',
            'especialidade',
            'foto',
            'media_avaliacoes',
            'total_avaliacoes',
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