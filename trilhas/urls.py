from django.urls import path

from .views import ( TrilhasListView,
    TrilhaDetalheView,
    TrilhaCreateView,
    TecnicaCreateView,
    TecnicaDetailView, 
    
)

urlpatterns = [
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
]


