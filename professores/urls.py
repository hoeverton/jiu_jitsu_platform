from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorCreateView,
    ProfessorDetailView,
    ProfessorUpdateView,
)

urlpatterns = [

    path('',ProfessorListView.as_view(),name='professor-list'),
    path('create/',ProfessorCreateView.as_view(),name='professor-create'),
    path('<int:pk>/',ProfessorDetailView.as_view(),name='professor-detail'),
    path('update/',ProfessorUpdateView.as_view(),name='professor-update'),
]