from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from professores.models import Professor
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from datetime import datetime, timedelta
from .models import Tecnica,Trilha,CategoriaTecnica
from .serializers import (
    TecnicaSerializer, 
    TrilhaSerializer, 
    CategoriaTecnicaSerializer 
    )

class TrilhasListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrilhaSerializer

    def get_queryset(self):
        professor = Professor.objects.get(
            user=self.request.user
        )

        return Trilha.objects.filter(
            professor=professor,
            ativa=True
        ).prefetch_related(
            'tecnicas'
        )



class TrilhaCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrilhaSerializer

    def perform_create(self, serializer):
        professor = Professor.objects.get(
            user=self.request.user
        )

        serializer.save(
            professor=professor
        )

class TecnicaCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TecnicaSerializer

    def perform_create(self, serializer):
        professor = Professor.objects.get(
            user=self.request.user
        )

        trilha = serializer.validated_data['trilha']

        if trilha.professor != professor:
            raise serializers.ValidationError(
                {
                    "trilha": "Você não pode adicionar técnicas a uma trilha de outro professor."
                }
            )

        categoria = serializer.validated_data.get('categoria')

        if categoria and categoria.trilha != trilha:
            raise serializers.ValidationError(
                {
                    "categoria": "A categoria precisa pertencer à mesma trilha."
                }
            )

        serializer.save()
        

class TrilhaDetalheView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrilhaSerializer

    def get_queryset(self):
        professor = Professor.objects.get(
            user=self.request.user
        )

        return Trilha.objects.filter(
            professor=professor,
            ativa=True
        ).prefetch_related(
            'tecnicas'
        )                 

class TecnicaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TecnicaSerializer

    def get_queryset(self):
        professor = Professor.objects.get(
            user=self.request.user
        )

        return Tecnica.objects.filter(
            trilha__professor=professor
        )


class CategoriaTecnicaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaTecnicaSerializer

    def get_queryset(self):
        professor = Professor.objects.get(
            user=self.request.user
        )

        trilha_id = self.kwargs['trilha_id']

        return CategoriaTecnica.objects.filter(
            trilha_id=trilha_id,
            trilha__professor=professor,
            ativa=True
        ).select_related(
            'trilha'
        ).order_by(
            'ordem',
            'nome'
        )

    def perform_create(self, serializer):
        professor = Professor.objects.get(
            user=self.request.user
        )

        trilha_id = self.kwargs['trilha_id']

        try:
            trilha = Trilha.objects.get(
                id=trilha_id,
                professor=professor,
                ativa=True
            )
        except Trilha.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "trilha": "Trilha não encontrada."
                }
            )

        serializer.save(
            trilha=trilha
        )

class CategoriaTecnicaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaTecnicaSerializer

    def get_queryset(self):
        professor = Professor.objects.get(user=self.request.user)

        return CategoriaTecnica.objects.filter(
            trilha__professor=professor
        )
  


