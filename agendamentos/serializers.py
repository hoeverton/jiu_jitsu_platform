from rest_framework import serializers

from .models import (
    RegraDisponibilidade,
    Disponibilidade,
    Agendamento,
)


class RegraDisponibilidadeSerializer(serializers.ModelSerializer):

    dia_semana_nome = serializers.CharField(
        source='get_dia_semana_display',
        read_only=True
    )

    class Meta:

        model = RegraDisponibilidade

        fields = [
            'id',
            'dia_semana',
            'dia_semana_nome',
            'hora_inicio',
            'hora_fim',
            'duracao_aula',
            'ativo',
            'criado_em',
        ]

        read_only_fields = [
            'id',
            'criado_em',
        ]

    def validate(self, attrs):

        hora_inicio = attrs.get(
            'hora_inicio',
            getattr(
                self.instance,
                'hora_inicio',
                None
            )
        )

        hora_fim = attrs.get(
            'hora_fim',
            getattr(
                self.instance,
                'hora_fim',
                None
            )
        )

        if (
            hora_inicio
            and hora_fim
            and hora_inicio >= hora_fim
        ):
            raise serializers.ValidationError({
                'hora_fim':
                    'O horário final deve ser maior que o horário inicial.'
            })

        return attrs


class DisponibilidadeSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Disponibilidade

        fields = [
            'id',
            'data',
            'hora_inicio',
            'hora_fim',
            'disponivel',
            'regra',
        ]

        read_only_fields = [
            'id',
            'regra',
        ]


class AgendamentoSerializer(
    serializers.ModelSerializer
):

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

    professor_foto = serializers.ImageField(
        source='professor.foto',
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
            'professor_foto',
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