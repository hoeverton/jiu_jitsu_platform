from rest_framework import generics
from .models import Professor
from .serializers import ProfessorSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from agendamentos.models import Agendamento
from avaliacoes.models import Avaliacao
from .models import Professor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Professor

class ProfessorListView(generics.ListAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'cidade',
        'especialidade',
        'faixa',
    ]

    search_fields = [
        'user__username',
        'especialidade',
        'cidade',
        'faixa',
    ]

    ordering_fields = [
        'preco_hora',
        'cidade',
        'faixa',
    ]


class ProfessorCreateView(generics.CreateAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

class ProfessorDetailView(generics.RetrieveAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ProfessorUpdateView(generics.UpdateAPIView):

    serializer_class = ProfessorSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return Professor.objects.get(user=self.request.user)   

class DashboardProfessorView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        professor = Professor.objects.get(
            user=request.user
        )

        pendentes = Agendamento.objects.filter(
            professor=professor,
            status='pendente'
        ).count()

        confirmados = Agendamento.objects.filter(
            professor=professor,
            status='confirmado'
        ).count()

        concluidos = Agendamento.objects.filter(
            professor=professor,
            status='concluido'
        ).count()

        avaliacoes = Avaliacao.objects.filter(
            professor=professor
        )

        media = avaliacoes.aggregate(
            Avg('nota')
        )['nota__avg']

        return Response({
            'agendamentos_pendentes': pendentes,
            'agendamentos_confirmados': confirmados,
            'agendamentos_concluidos': concluidos,
            'avaliacao_media': media or 0,
            'total_avaliacoes': avaliacoes.count()
        })  
       
class PerfilProfessorView(APIView):

    def get(self, request, professor_id):

        professor = Professor.objects.get(
            id=professor_id
        )

        avaliacoes = Avaliacao.objects.filter(
            professor=professor
        )

        media = avaliacoes.aggregate(
            Avg('nota')
        )['nota__avg']

        return Response({
            'id': professor.id,
            'nome': professor.user.username,
            'faixa': professor.faixa,
            'cidade': professor.cidade,
            'especialidade': professor.especialidade,
            'preco_hora': professor.preco_hora,
            'biografia': professor.biografia,
            'avaliacao_media': media or 0,
            'total_avaliacoes': avaliacoes.count()
        })