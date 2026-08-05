from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorCreateView,
    ProfessorDetailView,
    ProfessorUpdateView,
    DashboardProfessorView,
    PerfilProfessorView,
    
)

urlpatterns = [

    path('', ProfessorListView.as_view(), name='professor-list'),

    path('<int:pk>/', ProfessorDetailView.as_view(), name='professor-detail'),

    path('create/', ProfessorCreateView.as_view(), name='professor-create'),

    path('update/', ProfessorUpdateView.as_view(), name='professor-update'),

    path('dashboard/', DashboardProfessorView.as_view(), name='dashboard-professor'),

    path('perfil/<int:professor_id>/', PerfilProfessorView.as_view(), name='perfil-professor'),

]