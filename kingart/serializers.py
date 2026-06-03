from rest_framework import serializers
from .models import Comment
from . models import Blog,Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["blog"]


class BlogSerilizer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    image = serializers.ImageField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'image', 'title', 'content', 'created_at', 'user',"likes_count","is_liked",]

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        print("REQUEST:", request)
        print("USER:", request.user if request else None)
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                blog=obj,
                user=request.user
            ).exists()

        return False
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.image and request:
            data["image"] = request.build_absolute_uri(instance.image.url)

        return data




