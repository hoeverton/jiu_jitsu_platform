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
from .serializers import ProfessorSerializer

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

        if self.request.user.tipo_usuario != "professor":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Somente usuários cadastrados como professor podem criar um perfil profissional."
            )

        if Professor.objects.filter(user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError

            raise ValidationError(
                {
                    "detail": "Este usuário já possui um perfil de professor."
                }
            )

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
    
   

class ProfessorMeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            professor = Professor.objects.get(
                user=request.user
            )

        except Professor.DoesNotExist:
            return Response(
                {
                    "detail": "Perfil de professor não encontrado."
                },
                status=404
            )

        serializer = ProfessorSerializer(professor)

        return Response(serializer.data)
    

class ProfessorWhatsappView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, professor_id):

        try:
            professor = Professor.objects.get(
                id=professor_id
            )

        except Professor.DoesNotExist:
            return Response(
                {
                    "detail": "Professor não encontrado."
                },
                status=404
            )

        telefone = professor.user.telefone

        if not telefone:
            return Response(
                {
                    "detail": "Este professor não possui WhatsApp cadastrado."
                },
                status=404
            )

        return Response({
            "telefone": telefone
        })    