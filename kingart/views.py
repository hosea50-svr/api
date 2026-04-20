from django.shortcuts import render, get_object_or_404
from . models import Blog
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from . serializers import BlogSerilizer 

# Create your views here.

def test(request):
    blog = Blog.objects.all()
    return render(request, 'test.html', {'blogs':blog})
    
    #PYTHON API
    # return JsonResponse('hello', safe=False)
    # blog = Blog.objects.all().values('id','title','content')
    # print(blog)
   
    return JsonResponse(list(blog), safe=False)

def read(request,id):
    post = get_object_or_404(Blog, id=id)
    return render(request, 'read.html', {'post':post})

@api_view(['GET'])
@permission_classes([AllowAny]) 
def blog_list_api(request):
    post = Blog.objects.all()
    serializer = BlogSerilizer(post, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def post_blog_api(request):
    serializer = BlogSerilizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([AllowAny]) 
def put_blog_api(request,pk):
    post = post.objects.get(request,pk)
    serializer = BlogSerilizer(post,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,{'message':'working'})