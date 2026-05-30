from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from agendamentos.models import Agendamento


class DashboardAlunoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        aluno = request.user

        agendados = Agendamento.objects.filter(
            aluno=aluno,
            status='pendente'
        ).count()

        confirmados = Agendamento.objects.filter(
            aluno=aluno,
            status='confirmado'
        ).count()

        concluidos = Agendamento.objects.filter(
            aluno=aluno,
            status='concluido'
        ).count()

        cancelados = Agendamento.objects.filter(
            aluno=aluno,
            status='cancelado'
        ).count()
        professores_treinados = Agendamento.objects.filter(
            aluno=aluno,
            status='concluido'
        ).values(
            'professor'
        ).distinct().count()

        return Response({
            'agendamentos_pendentes': agendados,
            'agendamentos_confirmados': confirmados,
            'agendamentos_concluidos': concluidos,
            'agendamentos_cancelados': cancelados,
            'professores_treinados': professores_treinados,
        })