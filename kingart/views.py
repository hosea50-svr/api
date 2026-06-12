from django.shortcuts import render, get_object_or_404,redirect
from . models import Blog,Like
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from . serializers import BlogSerilizer
from . forms import BlogForm 
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings



from django.http import JsonResponse
import traceback

def get(self, request):
    try:
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if len(password) < 6:
            return Response({
                    "error":"Password must be at least 6 characters long"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username
            })
        
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

def test(request):
    blog = Blog.objects.all()
    return render(request, 'test.html', {'blog':blog})


def read(request,id):
    post = get_object_or_404(Blog, id=id)
    return render(request, 'read.html', {'post':post})

def update(request,id):
    blog_update = get_object_or_404(Blog, id=id)
    
    if request.method =="POST":
        form = BlogForm(request.POST,request.FILES,instance=blog_update)
        if form.is_valid():
            form.save()
            return redirect("read",id=blog_update.id)
        else:
            print("ERRORS",form.errors)
    else:
        form = BlogForm(instance=blog_update)
    return render(request,'update.html',{'form':form})



def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        blog.delete()
        return redirect("test")

    return render(request, "confirm_delete.html", {"blog": blog})

def post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('test') 
    else:
        form = BlogForm()

    return render(request, 'post.html', {'form': form})


def login(request):
    return render(request,"login.html")
    

# Class Bass API
class BlogListCreateAPIView(APIView):
    
    parser_classes = [MultiPartParser, FormParser]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()] 
        return [AllowAny()] 

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerilizer(blogs, many=True,context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        print(request.FILES)
        serializer = BlogSerilizer(data=request.data,context={"request": request})
        
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                "errors": serializer.errors,
                "message": "Failed to create post"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        


class BlogDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        try:
            return Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return None

    def get(self, request, id):
        blog = self.get_object(id)
        if blog is None:
            return Response({"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerilizer(blog,context={"request": request})
        return Response(serializer.data)

    # FULL UPDATE
    def put(self, request, id):
        blog = self.get_object(id)

        if blog is None:
            return Response({"message": "Blog not found"}, status=404)

        if blog.user_id != request.user.id:
            return Response({"error": "Not allowed"}, status=403)

        serializer = BlogSerilizer(blog, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # PARTIAL UPDATE (NEW)
    def patch(self, request, id):
        blog = self.get_object(id)

        if blog is None:
            return Response({"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        if blog.user_id != request.user.id:
            return Response({"error": "Not allowed"}, status=403)

        serializer = BlogSerilizer(
            blog,
            data=request.data,
            partial=True 
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        blog = self.get_object(id)

        if blog is None:
            return Response(
                {"message": "Post not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if blog.user_id != request.user.id:
            return Response({"error": "Not allowed"}, status=403)

        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#comment views
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(
            blog_id=self.kwargs["blog_id"]
        )

    def perform_create(self, serializer):
        serializer.save(
            blog_id=self.kwargs["blog_id"]
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def contact(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    full_message = f"""
    Name: {name}
    Email: {email}

    Message:
    {message}
    """

    send_mail(
        subject=f"New Contact Message from {name}",
        message=full_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["yourgmail@gmail.com"],
        fail_silently=False,
    )

    return Response({"message": "Email sent successfully"})


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        blog = Blog.objects.get(id=post_id)

        like = Like.objects.filter(
            user=request.user,
            blog=blog
        ).first()

        if like:
            like.delete()

            return Response({
                "message": "Post unliked",
                "liked": False,
                "likes_count": Like.objects.filter(blog=blog).count()
            })

        Like.objects.create(
            user=request.user,
            blog=blog
        )

        return Response({
            "message": "Post liked",
            "liked": True,
            "likes_count": Like.objects.filter(blog=blog).count()
        })


