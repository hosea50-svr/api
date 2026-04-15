from django.shortcuts import render, get_object_or_404
from . models import Blog


# Create your views here.

def test(request):
    blog = Blog.objects.all()
    return render(request, 'test.html', {'blogs':blog})


def read(request,id):
    post = get_object_or_404(Blog, id=id)
    return render(request, 'read.html', {'post':post})