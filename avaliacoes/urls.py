from django.urls import path
from .views import (
    AvaliacaoCreateView,
    ProfessorAvaliacoesView,
    
    )

urlpatterns = [

    path(
        'avaliacoes/create/',
        AvaliacaoCreateView.as_view(),
        name='avaliacao-create'
    ),
    path(
    'professores/<int:professor_id>/avaliacoes/',
    ProfessorAvaliacoesView.as_view(),
    name='professor-avaliacoes'
),
]