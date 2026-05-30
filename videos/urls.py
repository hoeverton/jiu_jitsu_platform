from django.urls import path
from .views import (
    VideoListView,
    VideoCreateView,
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
]