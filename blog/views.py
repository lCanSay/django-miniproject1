from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Post, Comment

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

def listall(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})