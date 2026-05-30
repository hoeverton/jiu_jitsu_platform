from django.urls import path
from .views import (
    VideoListView,
    VideoCreateView,
    ComprarVideoView,
    MeusVideosView,
)

urlpatterns = [

    path(
        'videos/',
        VideoListView.as_view(),
        name='video-list'
    ),

    path(
        'videos/create/',
        VideoCreateView.as_view(),
        name='video-create'
    ),

    path(
        'videos/<int:video_id>/comprar/',
        ComprarVideoView.as_view(),
        name='comprar-video'
    ),
    path(
        'meus-videos/',
        MeusVideosView.as_view(),
        name='meus-videos'
    ),


]