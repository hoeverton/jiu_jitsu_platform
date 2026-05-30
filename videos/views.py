from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer


class VideoListView(generics.ListAPIView):

    queryset = Video.objects.all()

    serializer_class = VideoSerializer


class VideoCreateView(generics.CreateAPIView):

    queryset = Video.objects.all()

    serializer_class = VideoSerializer