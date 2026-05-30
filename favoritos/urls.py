from django.urls import path
from .views import (
    FavoritarProfessorView,
    DesfavoritarProfessorView,
    FavoritosListView,
)

urlpatterns = [

    path(
        'professores/<int:professor_id>/favoritar/',
        FavoritarProfessorView.as_view(),
        name='favoritar-professor'
    ),

    path(
        'professores/<int:professor_id>/desfavoritar/',
        DesfavoritarProfessorView.as_view(),
        name='desfavoritar-professor'
    ),

    path(
        'favoritos/',
        FavoritosListView.as_view(),
        name='favoritos-list'
    ),
]