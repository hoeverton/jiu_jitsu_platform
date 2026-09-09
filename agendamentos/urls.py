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

    # Trilhas
    TrilhasListView,
    TrilhaDetalheView,
    TrilhaCreateView,
    TecnicaCreateView,
    TecnicaDetailView,

    # Progresso
    ProfessorAlunoProgressoView,
    MeuProgressoView,
    ProfessorAlunoTrilhaView,
   
)


urlpatterns = [

    # =========================================================
    # DISPONIBILIDADES
    # =========================================================

    path(
        'disponibilidades/',
        DisponibilidadeListView.as_view(),
        name='disponibilidade-list'
    ),

    path(
        'disponibilidades/create/',
        DisponibilidadeCreateView.as_view(),
        name='disponibilidade-create'
    ),


    # =========================================================
    # AGENDAMENTOS
    # =========================================================

    path(
        'agendamentos/create/',
        AgendamentoCreateView.as_view(),
        name='agendamento-create'
    ),

    path(
        'me/agendamentos/',
        MeusAgendamentosView.as_view(),
        name='meus-agendamentos'
    ),

    path(
        'professor/agendamentos/',
        ProfessorAgendamentosView.as_view(),
        name='professor-agendamentos'
    ),

    path(
        'agendamentos/<int:pk>/cancelar/',
        CancelarAgendamentoView.as_view(),
        name='cancelar-agendamento'
    ),

    path(
        'agendamentos/<int:pk>/confirmar/',
        ConfirmarAgendamentoView.as_view(),
        name='confirmar-agendamento'
    ),

    path(
        'agendamentos/<int:pk>/concluir/',
        ConcluirAgendamentoView.as_view(),
        name='concluir-agendamento'
    ),


    # =========================================================
    # DISPONIBILIDADES DO PROFESSOR
    # =========================================================

    path(
        'professores/<int:professor_id>/disponibilidades/',
        ProfessorDisponibilidadesView.as_view(),
        name='professor-disponibilidades'
    ),

    path(
        'disponibilidades/minhas/',
        MinhasDisponibilidadesView.as_view(),
        name='minhas-disponibilidades'
    ),

    path(
        'disponibilidades/minhas/<int:pk>/',
        MinhasDisponibilidadesDetailView.as_view(),
        name='minha-disponibilidade-detail'
    ),


    # =========================================================
    # HISTÓRICO DO ALUNO
    # =========================================================

    path(
        'alunos/historico/',
        HistoricoAlunoView.as_view(),
        name='historico-aluno'
    ),


    # =========================================================
    # REGRAS DE DISPONIBILIDADE
    # =========================================================

    path(
        'regras-disponibilidade/',
        RegraDisponibilidadeCreateView.as_view(),
        name='regra-disponibilidade-create'
    ),

    path(
        'regras-disponibilidade/minhas/',
        MinhasRegrasDisponibilidadeView.as_view(),
        name='minhas-regras-disponibilidade'
    ),


    # =========================================================
    # ALUNOS DO PROFESSOR
    # =========================================================

    path(
        'professor/alunos/',
        ProfessorAlunosView.as_view(),
        name='professor-alunos'
    ),

    path(
        'professor/alunos/<int:pk>/',
        ProfessorAlunoDetalheView.as_view(),
        name='professor-aluno-detalhe'
    ),


    # =========================================================
    # TRILHAS DE ESTUDO
    # =========================================================

    path(
        'trilhas/',
        TrilhasListView.as_view(),
        name='trilhas-list'
    ),

    path(
        'trilhas/<int:pk>/',
        TrilhaDetalheView.as_view(),
        name='trilha-detalhe'
    ),

    path(
        'trilhas/create/',
        TrilhaCreateView.as_view(),
        name='trilha-create'
    ),

    path(
        'tecnicas/create/',
        TecnicaCreateView.as_view(),
        name='tecnica-create'
    ),

    path(
        'tecnicas/<int:pk>/',
        TecnicaDetailView.as_view(),
        name='tecnica-detail'
    ),


    # =========================================================
    # PROGRESSO TÉCNICO DO ALUNO
    # =========================================================

    # GET  -> consulta progresso
    # POST -> cria/atualiza progresso
    path(
        'professor/alunos/<int:pk>/progresso/',
        ProfessorAlunoProgressoView.as_view(),
        name='professor-aluno-progresso'
    ),
    path(
        'meu-progresso/',
        MeuProgressoView.as_view(),
        name='meu-progresso'
    ),

    path(
        'professor/alunos/<int:pk>/trilha/',
        ProfessorAlunoTrilhaView.as_view(),
        name='professor-aluno-trilha'
    ),
    # PATCH -> altera uma técnica específica
   

]