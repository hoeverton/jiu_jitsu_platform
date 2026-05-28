from rest_framework import serializers
from .models import (
    Disponibilidade,
    Agendamento
)


class DisponibilidadeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Disponibilidade

        fields = [
                    'id',
                    'data',
                    'hora_inicio',
                    'hora_fim',
                    'disponivel',
                ]


class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Agendamento

        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Agendamento

        fields = [
            'id',
            'disponibilidade',
            'status',
            'criado_em',
        ]

        read_only_fields = [
            'status',
            'criado_em',
        ]
