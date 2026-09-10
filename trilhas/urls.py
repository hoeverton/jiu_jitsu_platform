from django.urls import path

from .views import ( TrilhasListView,
    TrilhaDetalheView,
    TrilhaCreateView,
    TecnicaCreateView,
    TecnicaDetailView, 
    CategoriaTecnicaListCreateView,
    CategoriaTecnicaDetailView,
    
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

    path(
    'trilhas/<int:trilha_id>/categorias/',
    CategoriaTecnicaListCreateView.as_view(),
    name='categoria-tecnica-list-create'
    ),

    path(
        'trilhas/<int:trilha_id>/categorias/<int:pk>/',
        CategoriaTecnicaDetailView.as_view(),
        name='categoria-tecnica-detail'
    ),
]


