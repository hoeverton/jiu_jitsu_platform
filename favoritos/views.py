from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from professores.models import Professor
from .models import Favorito
from .serializers import FavoritoSerializer

class FavoritarProfessorView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, professor_id):

        professor = Professor.objects.get(
            id=professor_id
        )

        favorito, created = Favorito.objects.get_or_create(
            aluno=request.user,
            professor=professor
        )

        return Response({
            'favoritado': True
        })
    
class DesfavoritarProfessorView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, professor_id):
        

        deletados, _ = Favorito.objects.filter(
            aluno=request.user,
            professor_id=professor_id
        ).delete()

        

        return Response({
            "favoritado": False
        })
class FavoritosListView(generics.ListAPIView):

    serializer_class = FavoritoSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Favorito.objects.filter(
            aluno=self.request.user
        )    