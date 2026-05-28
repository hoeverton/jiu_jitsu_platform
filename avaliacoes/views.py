from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Avaliacao
from .serializers import AvaliacaoSerializer
from agendamentos.models import Agendamento


class AvaliacaoCreateView(generics.CreateAPIView):

    serializer_class = AvaliacaoSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        agendamento = serializer.validated_data[
            'agendamento'
        ]

        if agendamento.aluno != self.request.user:

            raise serializers.ValidationError(
                'Você não pode avaliar este agendamento.'
            )

        if Avaliacao.objects.filter(
            agendamento=agendamento
        ).exists():

            raise serializers.ValidationError(
                'Este agendamento já foi avaliado.'
            )
        if agendamento.status != 'concluido':

            raise serializers.ValidationError(
                'A aula precisa estar concluída para ser avaliada.'
            )

        serializer.save(
            aluno=self.request.user,
            professor=agendamento.professor
        )

class ProfessorAvaliacoesView(generics.ListAPIView):

    serializer_class = AvaliacaoSerializer

    def get_queryset(self):

        professor_id = self.kwargs['professor_id']

        return Avaliacao.objects.filter(
            professor_id=professor_id
        ).order_by('-criado_em')        