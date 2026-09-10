from rest_framework import serializers
from .models import (
    Tecnica,
    Trilha,
    CategoriaTecnica,
    ProgressoAluno,
)


class TecnicaSerializer(serializers.ModelSerializer):

    categoria_nome = serializers.CharField(
        source='categoria.nome',
        read_only=True
    )

    class Meta:
        model = Tecnica

        fields = [
            'id',
            'trilha',
            'categoria',
            'categoria_nome',
            'nome',
            'descricao',
            'ordem',
            'ativa',
        ]

        read_only_fields = [
            'id',
            'categoria_nome',
        ]

    def validate(self, attrs):

        trilha = attrs.get(
            'trilha',
            getattr(
                self.instance,
                'trilha',
                None
            )
        )

        categoria = attrs.get(
            'categoria',
            getattr(
                self.instance,
                'categoria',
                None
            )
        )

        if categoria and trilha:
            if categoria.trilha_id != trilha.id:
                raise serializers.ValidationError({
                    'categoria':
                        'A categoria precisa pertencer à mesma trilha da técnica.'
                })

        return attrs
        
class TrilhaSerializer(serializers.ModelSerializer):

    tecnicas = TecnicaSerializer(
        many=True,
        read_only=True
    )

    total_tecnicas = serializers.SerializerMethodField()

    class Meta:
        model = Trilha

        fields = [
            'id',
            'nome',
            'descricao',
            'ordem',
            'ativa',
            'total_tecnicas',
            'tecnicas',
        ]

        read_only_fields = [
            'id',
            'total_tecnicas',
            'tecnicas',
        ]

    def get_total_tecnicas(self, obj):
        return obj.tecnicas.filter(
            ativa=True
        ).count()


class ProgressoAlunoSerializer(serializers.ModelSerializer):

    tecnica_nome = serializers.CharField(
        source='tecnica.nome',
        read_only=True
    )

    trilha_id = serializers.IntegerField(
        source='tecnica.trilha.id',
        read_only=True
    )

    trilha_nome = serializers.CharField(
        source='tecnica.trilha.nome',
        read_only=True
    )

    categoria_id = serializers.IntegerField(
        source='tecnica.categoria.id',
        read_only=True
    )

    categoria_nome = serializers.CharField(
        source='tecnica.categoria.nome',
        read_only=True
    )

    class Meta:
        model = ProgressoAluno

        fields = [
            'id',
            'aluno',
            'tecnica',
            'tecnica_nome',
            'trilha_id',
            'trilha_nome',
            'categoria_id',
            'categoria_nome',
            'aprendido',
            'atualizado_em',
        ]

        read_only_fields = [
            'id',
            'tecnica_nome',
            'trilha_id',
            'trilha_nome',
            'atualizado_em',
        ]       
class CategoriaTecnicaSerializer(serializers.ModelSerializer):

    class Meta:

        model = CategoriaTecnica

        fields = [
            'id',
            'trilha',
            'nome',
            'ordem',
            'ativa',
            'criado_em',
        ]

        read_only_fields = [
            'id',
            'criado_em',
        ]
