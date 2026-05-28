from rest_framework import serializers
from .models import Professor


class ProfessorSerializer(serializers.ModelSerializer):

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
        ]