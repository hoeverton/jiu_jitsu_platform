from rest_framework import generics
from .models import Professor
from .serializers import ProfessorSerializer
from rest_framework.permissions import IsAuthenticated



class ProfessorListView(generics.ListAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filterset_fields = [
        'cidade',
        'especialidade',
        'faixa',
    ]

    search_fields = [
        'user__username',
        'especialidade',
        'cidade',
        'faixa',
    ]

    ordering_fields = [
        'preco_hora',
        'cidade',
        'faixa',
    ]


class ProfessorCreateView(generics.CreateAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

class ProfessorDetailView(generics.RetrieveAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ProfessorUpdateView(generics.UpdateAPIView):

    serializer_class = ProfessorSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return Professor.objects.get(user=self.request.user)    
