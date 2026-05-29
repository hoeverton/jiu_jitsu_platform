from django.urls import path
from .views import DashboardAlunoView

urlpatterns = [
    path('dashboard/',DashboardAlunoView.as_view(),name='dashboard-aluno'),

]