from rest_framework import serializers
from .models import Video
from .models import Video, CompraVideo


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'



class VideoSerializer(serializers.ModelSerializer):

    url_youtube = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_url_youtube(self, obj):

        request = self.context.get('request')

        if obj.gratuito:
            return obj.url_youtube

        if request and request.user.is_authenticated:

            comprou = CompraVideo.objects.filter(
                aluno=request.user,
                video=obj
            ).exists()

            if comprou:
                return obj.url_youtube

        return None
