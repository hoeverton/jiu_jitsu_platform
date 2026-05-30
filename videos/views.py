from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Video, CompraVideo




class VideoListView(generics.ListAPIView):

    queryset = Video.objects.all()

    serializer_class = VideoSerializer


class VideoCreateView(generics.CreateAPIView):

    queryset = Video.objects.all()

    serializer_class = VideoSerializer

class ComprarVideoView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):

        video = Video.objects.get(id=video_id)

        compra, criada = CompraVideo.objects.get_or_create(
            aluno=request.user,
            video=video
        )

        return Response({
            'comprado': True,
            'video': video.titulo
        })    
    
class MeusVideosView(generics.ListAPIView):

    serializer_class = VideoSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(
            compravideo__aluno=self.request.user
        ).distinct()

    def get_serializer_context(self):
        return {'request': self.request}  