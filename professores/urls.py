from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorCreateView,
    ProfessorDetailView,
    ProfessorUpdateView,
    DashboardProfessorView,
    PerfilProfessorView,
    ProfessorDetalheView,
)

urlpatterns = [

    path('',ProfessorListView.as_view(),name='professor-list'),
    path('create/',ProfessorCreateView.as_view(),name='professor-create'),
    path('<int:pk>/',ProfessorDetailView.as_view(),name='professor-detail'),
    path('update/',ProfessorUpdateView.as_view(),name='professor-update'),
    path('dashboard/',DashboardProfessorView.as_view(),name='dashboard-professor'),
    path('<int:professor_id>/',PerfilProfessorView.as_view(),name='perfil-professor'),
    path('<int:pk>/',ProfessorDetalheView.as_view(),name='professor-detalhe'),
]