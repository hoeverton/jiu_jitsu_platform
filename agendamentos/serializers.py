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

    aluno_nome = serializers.CharField(
        source='aluno.username',
        read_only=True
    )

    professor_id = serializers.IntegerField(
        source='professor.id',
        read_only=True
    )

    professor_nome = serializers.CharField(
        source='professor.user.username',
        read_only=True
    )

    data = serializers.DateField(
        source='disponibilidade.data',
        read_only=True
    )

    hora_inicio = serializers.TimeField(
        source='disponibilidade.hora_inicio',
        read_only=True
    )

    hora_fim = serializers.TimeField(
        source='disponibilidade.hora_fim',
        read_only=True
    )

    class Meta:

        model = Agendamento

        fields = [
            'id',
            'aluno_nome',
            'professor_id',
            'professor_nome',
            'disponibilidade',
            'data',
            'hora_inicio',
            'hora_fim',
            'status',
            'criado_em',
        ]

        read_only_fields = [
            'status',
            'criado_em',
            'aluno_nome',
            'professor_id',
            'professor_nome',
            'data',
            'hora_inicio',
            'hora_fim',
        ]