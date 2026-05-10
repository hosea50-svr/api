from rest_framework import serializers
from . models import Blog

class BlogSerilizer(serializers.ModelSerializer):

    image = serializers.ImageField()

    class Meta:
        model = Blog
        fields = ['id', 'image', 'title', 'content', 'created_at', 'user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.image and request:
            data["image"] = request.build_absolute_uri(instance.image.url)

        return data
