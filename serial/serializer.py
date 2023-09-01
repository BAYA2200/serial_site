from rest_framework import serializers

from serial.models import TVShow, Comment


class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('tvshow', )

