from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment
import requests
import json



def index(request):
    secrets = json.loads(open('secrets.json').read())
    api_key = secrets['API_KEY']
    now_playing_url = 'https://api.themoviedb.org/3/movie/now_playing?api_key={}&language=ko-KR&page=1,region=KR'.format(api_key)
    now_playing_response = requests.get(now_playing_url).json()
    now_playing = sorted(now_playing_response['results'], key=lambda x:x['vote_average'], reverse=True)[:5]

    top_rated_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=ko-KR&page=1'.format(api_key)
    top_rated_response = requests.get(top_rated_url).json()
    top_rated = sorted(top_rated_response['results'], key=lambda x:x['vote_average'], reverse=True)[:5]
    context = {
        'now_playing': now_playing,
        'top_rated': top_rated,
    }
    return render(request, 'posts/index.html', context)


# tmdb API를 이용하여 검색한 결과를 가져와 상세정보 출력
def search(request):
    TMDB_API_KEY = 'caea966f6e10b1fbcfc446cd0052d5cd'

    movie_title = request.GET.get('title')

    url ='https://api.themoviedb.org/3/search/movie'

    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_title,
        'language': 'ko-kr',
    }

    response = requests.get(url, params=params)
    search_data = response.json()

    image_url = 'https://image.tmdb.org/t/p/w200' # w로 사이즈 조절
    for movie in search_data['results']:
        if movie['poster_path']:
            movie['poster_path'] = image_url + movie['poster_path']
        else:
            movie['poster_path'] = '이미지 없음'


    context = {
        'search_data': search_data
    }

    return render(request, 'posts/search.html', context)


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