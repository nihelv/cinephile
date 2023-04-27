from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/test.html')


def movie_detail(request):
    pass


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/create.html', context)


@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post.pk)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
    }
    return render(request, 'posts/update.html', context)


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
        return redirect('posts:movie_detail')


@login_required
def post_likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:post_detail', post.pk)


@login_required
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:post_detail', post.pk)


@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:post_detail', post_pk)


@login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Post.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:post_detail', post_pk)