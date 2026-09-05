from django.urls import path
from .views import (
    DisponibilidadeListView,
    DisponibilidadeCreateView,
    AgendamentoCreateView,
    MeusAgendamentosView,
    ProfessorAgendamentosView,
    CancelarAgendamentoView,
    ConfirmarAgendamentoView,
    ConcluirAgendamentoView,
    ProfessorDisponibilidadesView,
    HistoricoAlunoView,
    MinhasDisponibilidadesView,
    MinhasDisponibilidadesDetailView,
    RegraDisponibilidadeCreateView,
    MinhasRegrasDisponibilidadeView,
    ProfessorAlunosView,
    ProfessorAlunoDetalheView,
    TrilhasListView,
    TrilhaDetalheView,
    ProfessorAlunoProgressoView,
    TrilhaCreateView,
    TecnicaCreateView,
)

urlpatterns = [

    path('disponibilidades/',DisponibilidadeListView.as_view(),
         name='disponibilidade-list'),
    path('disponibilidades/create/',DisponibilidadeCreateView.as_view(),
         name='disponibilidade-create'),
    path('agendamentos/create/',AgendamentoCreateView.as_view(),
         name='agendamento-create'),
    path('me/agendamentos/',MeusAgendamentosView.as_view(),
         name='meus-agendamentos'),
    path('professor/agendamentos/',ProfessorAgendamentosView.as_view(),
         name='professor-agendamentos'),     
    path('agendamentos/<int:pk>/cancelar/',CancelarAgendamentoView.as_view(),
         name='cancelar-agendamento'),
    path('agendamentos/<int:pk>/confirmar/',ConfirmarAgendamentoView.as_view(),
          name='confirmar-agendamento'),      
    path('agendamentos/<int:pk>/concluir/',ConcluirAgendamentoView.as_view(),
         name='concluir-agendamento'),
    path('professores/<int:professor_id>/disponibilidades/',ProfessorDisponibilidadesView.as_view(),
        name='professor-disponibilidades'),
    path('alunos/historico/',HistoricoAlunoView.as_view(),
        name='historico-aluno'),
    path('disponibilidades/minhas/',MinhasDisponibilidadesView.as_view(),
        name='minhas-disponibilidades'), 
    path('disponibilidades/minhas/<int:pk>/',MinhasDisponibilidadesDetailView.as_view(),
        name='minha-disponibilidade-detail'),
    path('regras-disponibilidade/',RegraDisponibilidadeCreateView.as_view(),
        name='regra-disponibilidade-create'),

    path('regras-disponibilidade/minhas/',MinhasRegrasDisponibilidadeView.as_view(),
        name='minhas-regras-disponibilidade'),

    path('professor/alunos/',ProfessorAlunosView.as_view(),
        name='professor-alunos'),  

    path("professor/alunos/<int:pk>/",ProfessorAlunoDetalheView.as_view(),
        name="professor-aluno-detalhe"),

    path('trilhas/',TrilhasListView.as_view(),
        name='trilhas-list'),

    path('trilhas/<int:pk>/',TrilhaDetalheView.as_view(),
        name='trilha-detalhe'),

    path('professor/alunos/<int:pk>/progresso/',ProfessorAlunoProgressoView.as_view(),
        name='professor-aluno-progresso'), 

    path('trilhas/create/',TrilhaCreateView.as_view(),
        name='trilha-create'),

    path('tecnicas/create/',TecnicaCreateView.as_view(),
        name='tecnica-create'),                          
                
]