from django.shortcuts import render, get_object_or_404
from . models import Blog
from django.http import JsonResponse

# Create your views here.

def test(request):
    # blog = Blog.objects.all()
    # return render(request, 'test.html', {'blogs':blog})

    #PYTHON API
    blog = Blog.objects.all().values('id','title','content')
    print(blog)
    # return JsonResponse('hello', safe=False)
    return JsonResponse(list(blog), safe=False)

def read(request,id):
    post = get_object_or_404(Blog, id=id)
    return render(request, 'read.html', {'post':post})