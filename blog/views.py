from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

def listall(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_own_post = post.author == request.user
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('postapp:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post, 
        'is_own_post': is_own_post,
        'comments': comments,
        'form': form,
        })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('postapp:post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('postapp:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('postapp:listofposts')
    return redirect('postapp:post_detail', post_id=post_id)