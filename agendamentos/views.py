from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from professores.models import Professor
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from datetime import datetime, timedelta


from .models import (
    Disponibilidade,
    Agendamento,
    RegraDisponibilidade,
    Trilha,
    Tecnica,
    ProgressoAluno,
)

from .serializers import (
    DisponibilidadeSerializer,
    AgendamentoSerializer,
    RegraDisponibilidadeSerializer,
    TrilhaSerializer,
    TecnicaSerializer,
    ProgressoAlunoSerializer,
)

def gerar_disponibilidades_professor(professor, dias=30):
    """
    Gera horários individuais de aula para os próximos X dias
    com base nas regras semanais do professor.
    """

    hoje = timezone.localdate()

    data_final = hoje + timedelta(days=dias)

    regras = RegraDisponibilidade.objects.filter(
        professor=professor,
        ativo=True
    )

    for regra in regras:

        data_atual = hoje

        while data_atual <= data_final:

            # Segunda = 0
            # Terça = 1
            # ...
            # Domingo = 6

            if data_atual.weekday() == regra.dia_semana:

                hora_atual = regra.hora_inicio

                while True:

                    inicio_datetime = datetime.combine(
                        data_atual,
                        hora_atual
                    )

                    fim_datetime = (
                        inicio_datetime
                        + timedelta(minutes=regra.duracao_aula)
                    )

                    limite_datetime = datetime.combine(
                        data_atual,
                        regra.hora_fim
                    )

                    # Não cria uma aula que ultrapasse
                    # o horário final do professor
                    if fim_datetime > limite_datetime:
                        break

                    hora_inicio = inicio_datetime.time()
                    hora_fim = fim_datetime.time()

                    # Cria somente o horário individual
                    Disponibilidade.objects.get_or_create(
                        professor=professor,
                        data=data_atual,
                        hora_inicio=hora_inicio,
                        hora_fim=hora_fim,
                        defaults={
                            "disponivel": True,
                            "regra": regra,
                        }
                    )

                    hora_atual = hora_fim

            data_atual += timedelta(days=1)


class DisponibilidadeListView(APIView):

    def get(self, request):

        professor_id = request.query_params.get(
            "professor"
        )

        if professor_id:

            try:

                professor = Professor.objects.get(
                    id=professor_id
                )

            except Professor.DoesNotExist:

                return Response(
                    {
                        "detail":
                        "Professor não encontrado."
                    },
                    status=404
                )

            gerar_disponibilidades_professor(
                professor,
                dias=30
            )

            disponibilidades = (
                Disponibilidade.objects.filter(
                    professor=professor,
                    disponivel=True
                )
            )

        else:

            disponibilidades = (
                Disponibilidade.objects.filter(
                    disponivel=True
                )
            )

        disponibilidades = (
            disponibilidades
            .filter(data__gte=timezone.localdate())
            .order_by(
                "data",
                "hora_inicio"
            )
        )

        dias = defaultdict(list)

        for disponibilidade in disponibilidades:

            dias[
                disponibilidade.data.strftime(
                    "%Y-%m-%d"
                )
            ].append(
                {
                    "id": disponibilidade.id,

                    "hora_inicio":
                        disponibilidade.hora_inicio.strftime(
                            "%H:%M"
                        ),

                    "hora_fim":
                        disponibilidade.hora_fim.strftime(
                            "%H:%M"
                        ),
                }
            )

        resultado = []

        for data, horarios in dias.items():

            resultado.append(
                {
                    "data": data,
                    "horarios": horarios,
                }
            )

        return Response(resultado)

class DisponibilidadeCreateView(generics.CreateAPIView):

    serializer_class = DisponibilidadeSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        professor = Professor.objects.get(
            user=request.user
        )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        data_disponibilidade = data["data"]
        hora_inicio = data["hora_inicio"]
        hora_fim = data["hora_fim"]

        horarios_criados = []

        inicio_datetime = datetime.combine(
            data_disponibilidade,
            hora_inicio
        )

        limite_datetime = datetime.combine(
            data_disponibilidade,
            hora_fim
        )

        while True:

            fim_datetime = (
                inicio_datetime
                + timedelta(minutes=60)
            )

            if fim_datetime > limite_datetime:
                break

            disponibilidade, created = (
                Disponibilidade.objects.get_or_create(
                    professor=professor,
                    data=data_disponibilidade,
                    hora_inicio=inicio_datetime.time(),
                    hora_fim=fim_datetime.time(),
                    defaults={
                        "disponivel": True,
                    }
                )
            )

            horarios_criados.append(
                disponibilidade
            )

            inicio_datetime = fim_datetime

        serializer_data = (
            DisponibilidadeSerializer(
                horarios_criados,
                many=True
            ).data
        )

        return Response(
            serializer_data,
            status=201
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
    
class ProfessorAlunosView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        professor = Professor.objects.get(
            user=request.user
        )

        agendamentos = (
            Agendamento.objects
            .filter(professor=professor)
            .select_related(
                'aluno',
                'disponibilidade'
            )
            .order_by('-disponibilidade__data',
                      '-disponibilidade__hora_inicio')
        )

        alunos = {}

        for agendamento in agendamentos:

            aluno = agendamento.aluno

            if aluno.id not in alunos:

                alunos[aluno.id] = {
                    'id': aluno.id,
                    'nome': aluno.username,
                    'email': aluno.email,
                    'foto': (
                        aluno.foto.url
                        if aluno.foto
                        else None
                    ),
                    'total_aulas': 0,
                    'aulas_concluidas': 0,
                    'ultima_aula': None,
                    'proxima_aula': None,
                }

            dados = alunos[aluno.id]

            dados['total_aulas'] += 1

            if agendamento.status == 'concluido':
                dados['aulas_concluidas'] += 1

            data = (
                agendamento.disponibilidade.data
            )

            hora = (
                agendamento.disponibilidade.hora_inicio
            )

            data_hora = datetime.combine(
                data,
                hora
            )

            agora = timezone.localtime().replace(
                tzinfo=None
            )

            if data_hora <= agora:

                if (
                    dados['ultima_aula'] is None
                    or data_hora >
                    datetime.fromisoformat(
                        dados['ultima_aula']
                    )
                ):

                    dados['ultima_aula'] = (
                        data_hora.isoformat()
                    )

            elif (
                dados['proxima_aula'] is None
                or data_hora <
                datetime.fromisoformat(
                    dados['proxima_aula']
                )
            ):

                dados['proxima_aula'] = (
                    data_hora.isoformat()
                )

        return Response(
            list(alunos.values())
        ) 
class ProfessorAlunoDetalheView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        professor = Professor.objects.get(
            user=request.user
        )

        # Procura um agendamento deste professor
        # com o aluno informado
        primeiro_agendamento = (
            Agendamento.objects
            .filter(
                professor=professor,
                aluno_id=pk
            )
            .select_related(
                'aluno',
                'disponibilidade'
            )
            .first()
        )

        if not primeiro_agendamento:
            return Response(
                {"detail": "Aluno não encontrado."},
                status=404
            )

        aluno = primeiro_agendamento.aluno

        agendamentos = (
            Agendamento.objects
            .filter(
                professor=professor,
                aluno=aluno
            )
            .select_related(
                'disponibilidade'
            )
            .order_by(
                '-disponibilidade__data',
                '-disponibilidade__hora_inicio'
            )
        )

        historico = []

        for agendamento in agendamentos:
            disponibilidade = agendamento.disponibilidade

            historico.append({
                "id": agendamento.id,
                "data": disponibilidade.data,
                "hora_inicio": disponibilidade.hora_inicio,
                "hora_fim": disponibilidade.hora_fim,
                "status": agendamento.status,
            })

        return Response({
            "id": aluno.id,
            "nome": aluno.username,
            "email": aluno.email,
            "foto": (
                aluno.foto.url
                if aluno.foto
                else None
            ),
            "total_aulas": agendamentos.count(),
            "aulas_concluidas": agendamentos.filter(
                status="concluido"
            ).count(),
            "historico": historico,
        })
    
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
    
class MinhasDisponibilidadesView(generics.ListAPIView):

    serializer_class = DisponibilidadeSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return Disponibilidade.objects.filter(
            professor=professor
        ).order_by(
            'data',
            'hora_inicio'
        )    

class MinhasDisponibilidadesDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = DisponibilidadeSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return Disponibilidade.objects.filter(
            professor=professor
        )
    
class RegraDisponibilidadeCreateView(generics.CreateAPIView):

    serializer_class = (RegraDisponibilidadeSerializer)

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        professor = Professor.objects.get(
            user=self.request.user
        )

        serializer.save(
            professor=professor
        )   

class MinhasRegrasDisponibilidadeView(generics.ListAPIView):

    serializer_class = (RegraDisponibilidadeSerializer)

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        return RegraDisponibilidade.objects.filter(
            professor=professor
        ).order_by(
            'dia_semana',
            'hora_inicio'
        )

class TrilhasListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Trilha.objects.filter(
        ativa=True
    ).prefetch_related('tecnicas')

    serializer_class = TrilhaSerializer


class TrilhaDetalheView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Trilha.objects.filter(
        ativa=True
    ).prefetch_related('tecnicas')

    serializer_class = TrilhaSerializer


class ProfessorAlunoProgressoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ProgressoAlunoSerializer

    def get_queryset(self):

        professor = Professor.objects.get(
            user=self.request.user
        )

        aluno_id = self.kwargs['pk']

        return ProgressoAluno.objects.filter(
            aluno_id=aluno_id,
            tecnica__trilha__ativa=True
        ).select_related(
            'tecnica',
            'tecnica__trilha'
        )