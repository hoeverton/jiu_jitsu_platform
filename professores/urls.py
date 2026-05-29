from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorCreateView,
    ProfessorDetailView,
    ProfessorUpdateView,
    DashboardProfessorView,
)

urlpatterns = [

    path('',ProfessorListView.as_view(),name='professor-list'),
    path('create/',ProfessorCreateView.as_view(),name='professor-create'),
    path('<int:pk>/',ProfessorDetailView.as_view(),name='professor-detail'),
    path('update/',ProfessorUpdateView.as_view(),name='professor-update'),
    path('dashboard/',DashboardProfessorView.as_view(),name='dashboard-professor'),
]