from rest_framework import serializers
from vox.models import Topic, Post

class LastPostSerializer(serializers.Serializer):
    author = serializers.StringRelatedField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

class TopicSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(default=0, read_only=True)
    likes_num = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    last_post = LastPostSerializer(read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    text = serializers.CharField(write_only=True)

    class Meta:
        model = Topic
        fields = ("id", "slug", "text", "title", "created", "author", "likes_num", "liked", "last_post", "category")

class PostSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(default=0, read_only=True)
    likes_num = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "text", "created", "likes_num", "liked", "topic")
