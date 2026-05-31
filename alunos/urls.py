from django.urls import path
from .views import (
    DashboardAlunoView,
    BibliotecaAlunoView,
)
urlpatterns = [
    path('dashboard/',DashboardAlunoView.as_view(),name='dashboard-aluno'),
    path('biblioteca/', BibliotecaAlunoView.as_view(),name='biblioteca-aluno'),

]