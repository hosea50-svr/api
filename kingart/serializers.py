from rest_framework import serializers
from . models import Blog

class BlogSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','content','created_at']