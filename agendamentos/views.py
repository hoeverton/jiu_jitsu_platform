from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from professores.models import Professor
from django.utils import timezone

from .models import (
    Disponibilidade,
    Agendamento
)

from .serializers import (
    DisponibilidadeSerializer,
    AgendamentoSerializer
)


class DisponibilidadeListView(generics.ListAPIView):

    queryset = Disponibilidade.objects.all()

    serializer_class = DisponibilidadeSerializer


class DisponibilidadeCreateView(generics.CreateAPIView):

    serializer_class = DisponibilidadeSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        professor = Professor.objects.get(
            user=self.request.user
        )

        serializer.save(
            professor=professor
        )

class AgendamentoCreateView(generics.CreateAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        disponibilidade = serializer.validated_data[
            'disponibilidade'
        ]

        if not disponibilidade.disponivel:

            raise serializers.ValidationError(
                'Horário indisponível.'
            )

        disponibilidade.disponivel = False

        disponibilidade.save()

        serializer.save(
            aluno=self.request.user,
            professor=disponibilidade.professor
        )

class MeusAgendamentosView(generics.ListAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Agendamento.objects.filter(
            aluno=self.request.user
        )        

class ProfessorAgendamentosView(generics.ListAPIView):

    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        queryset = Agendamento.objects.filter(
            professor=professor
        )

        status = self.request.query_params.get(
            'status'
        )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset.order_by('-id')
    
class CancelarAgendamentoView(generics.UpdateAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    http_method_names = ['patch']

    def get_object(self):

        return Agendamento.objects.get(
            id=self.kwargs['pk'],
            aluno=self.request.user
        )

    def perform_update(self, serializer):

        agendamento = self.get_object()

        disponibilidade = agendamento.disponibilidade

        disponibilidade.disponivel = True

        disponibilidade.save()

        serializer.save(
            status='cancelado'
        ) 

class ConfirmarAgendamentoView(generics.UpdateAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    http_method_names = ['patch']

    def get_object(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return Agendamento.objects.get(
            id=self.kwargs['pk'],
            professor=professor
        )

    def perform_update(self, serializer):

        serializer.save(
            status='confirmado'
        )   

class ConcluirAgendamentoView(generics.UpdateAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    http_method_names = ['patch']

    def get_object(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return Agendamento.objects.get(
            id=self.kwargs['pk'],
            professor=professor
        )

    def perform_update(self, serializer):

        serializer.save(
            status='concluido'
        )             

class ProfessorDisponibilidadesView(generics.ListAPIView):

    serializer_class = DisponibilidadeSerializer

    def get_queryset(self):

        professor_id = self.kwargs['professor_id']

        return Disponibilidade.objects.filter(
            professor_id=professor_id,
            disponivel=True
        ).order_by('data', 'hora_inicio')
    
class HistoricoAlunoView(generics.ListAPIView):

    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Agendamento.objects.filter(
            aluno=self.request.user,
            status='concluido'
        ).order_by('-id')            

class AgendaProfessorView(generics.ListAPIView):

    serializer_class = AgendamentoSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return Agendamento.objects.filter(
            professor=professor,
            status='confirmado'
        ).order_by('id')