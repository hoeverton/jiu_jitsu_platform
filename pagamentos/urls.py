from django.urls import path
from .views import CriarPixView

urlpatterns = [
    path(
        'criar-pix/',CriarPixView.as_view(),
            name='criar-pix'),
]