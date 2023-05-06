from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator
# from django.http import HttpResponseRedirect
import requests
import random, datetime
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

def index(request):
    # 최신 상영작을 평점 순으로 나열하여 5개만 불러옵니다.
    now_playing_url = 'https://api.themoviedb.org/3/movie/now_playing'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-kr',
        'region':'kr',
        'page': 1
    }
    now_playing_response = requests.get(now_playing_url, params=params)
    now_playing_data = now_playing_response.json()
    now_playing = sorted(now_playing_data['results'], key=lambda x:x['vote_average'], reverse=True)[:5]

    # 명작 영화를 평점 순으로 나열하여 5개만 불러옵니다.
    top_rated_url = 'https://api.themoviedb.org/3/movie/top_rated'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-kr',
        'region':'kr',
        'page': 1
    }

    top_rated_response = requests.get(top_rated_url, params=params)
    top_rated_data = top_rated_response.json()
    top_rated = sorted(top_rated_data['results'], key=lambda x:x['vote_average'], reverse=True)[:5]
    
    # 장르 번호를 딕셔너리로 만들어두었으니 활용하시면 됩니다.
    genre_dict = {
        28: '액션',
        12: '모험',
        16: '애니메이션',
        35: '코미디',
        80: '범죄',
        99: '다큐멘터리',
        18: '드라마',
        10751: '가족',
        14: '판타지',
        36: '역사',
        27: '공포',
        10402: '음악',
        9648: '미스터리',
        10749: '로맨스',
        878: 'SF',
        10770: 'TV 영화',
        53: '스릴러',
        10752: '전쟁',
        37: '서부'
    }
    
    # 장르별 영화를 불러옵니다.
    # 템플릿에서 genre_ids에 원하는 장르 번호가 있는지 확인하여 장르별 영화를 불러올 수 있습니다.
    # 단, 평균적으로 5개 이상의 장르별 영화를 불러오려면 여러 개 페이지를 참여해야 하므로 for문을 사용했습니다.
    # 템플릿에서는 페이지별 영화정보를 불러오는 for문, 한 페이지의 영화정보들에서 하나씩 영화 정보를 불러오는 for문, 이렇게 2중 for문을 사용해야 합니다.
    genre_movie_list = list()
    for page in range(1, 5):
        genre_url = 'https://api.themoviedb.org/3/movie/top_rated'

        params = {
            'api_key': TMDB_API_KEY,
            'language': 'ko-kr',
            'region':'kr',
            'page': page
        }

        genre_response = requests.get(genre_url, params=params)
        genre_data = genre_response.json()
        genre = sorted(genre_data['results'], key=lambda x:x['vote_average'], reverse=True)
        genre_movie_list.append(genre)


    # 랜덤 영화 추천
    random_url = 'https://api.themoviedb.org/3/discover/movie'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-kr',
        'region': 'kr',
        'page': random.randrange(1, 500)
    }

    random_response = requests.get(random_url, params=params)
    random_data = random_response.json()
    random_movie = random.choice(random_data['results'])

    # 상영예정작 영화를 5개만 불러옵니다.
    upcoming_url = 'https://api.themoviedb.org/3/movie/upcoming'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-kr',
        'region':'kr',
        'page': 1
    }

    upcoming_response = requests.get(upcoming_url, params=params)
    upcoming_data = upcoming_response.json()
    upcoming_movies = sorted(upcoming_data['results'], key=lambda x:x['release_date'])[:5]
    current_date = datetime.date.today()

    upcoming_movies_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}

    for i in range(5):
        movie_id = upcoming_movies[i]['id']
        upcoming_movies_dict[i]['id'] = upcoming_movies[i]['id']
        upcoming_movies_dict[i]['poster_path'] = upcoming_movies[i]['poster_path']
        upcoming_movies_dict[i]['title'] = upcoming_movies[i]['title']
        upcoming_movies_dict[i]['genre_ids'] = upcoming_movies[i]['genre_ids']

        release_dates_url = f'https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={TMDB_API_KEY}'
        release_dates_response = requests.get(release_dates_url)
        release_data = release_dates_response.json()

        for data in release_data['results']:
            if data["iso_3166_1"] == "KR":
                release_date = data["release_dates"][-1].get("release_date")
                break

        year = int(release_date[:4])
        month = int(release_date[5:7])
        day = int(release_date[8:10])
        upcoming_movies_dict[i]['day'] = (datetime.date(year, month, day) - datetime.date.today()).days

    context = {
        'now_playing': now_playing,
        'top_rated': top_rated,
        'genre_movie_list': genre_movie_list,
        'random_movie': random_movie,
        'upcoming_movies_dict': upcoming_movies_dict,
        'current_date': current_date,
        'genre_dict': genre_dict,
        'login_form': CustomAuthenticationForm(),
        'signup_form': CustomUserCreationForm(),
    }
    return render(request, 'posts/index.html', context)


# tmdb API를 이용하여 검색한 결과를 가져와 상세정보 출력
def search(request):
    query = request.GET.get('query')

    movie_url = 'https://api.themoviedb.org/3/search/movie'
    person_url = 'https://api.themoviedb.org/3/search/person'

    movie_params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'ko-kr',
    }

    person_params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'ko-kr',
    }

    movie_response = requests.get(movie_url, params=movie_params)
    person_response = requests.get(person_url, params=person_params)

    movie_search_data = movie_response.json()
    person_search_data = person_response.json()

    movie_image_url = 'https://image.tmdb.org/t/p/w200'  # w로 사이즈 조절
    for movie in movie_search_data['results']:
        if movie['poster_path']:
            movie['poster_path'] = movie_image_url + movie['poster_path']

    person_image_url = 'https://image.tmdb.org/t/p/w200'
    for person in person_search_data['results']:
        if person.get('profile_path'):
            person['profile_path'] = person_image_url + person['profile_path']

    
    # 검색한 배우의 출연 영화 목록
    movies_cast = []
    movie_posters = []
    movies = []

    if 'results' in person_search_data and person_search_data['results']:
        for person in person_search_data['results']:
            if person.get('profile_path'):
                person_id = person['id']
                credit_url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits"
                credit_params = {
                    'api_key': TMDB_API_KEY,
                    'language': 'ko-kr',
                }
                credit_response = requests.get(credit_url, params=credit_params)
                credit_data = credit_response.json()

                movies = []
                if 'cast' in credit_data:
                    sorted_actor_movies = sorted(credit_data['cast'], key=lambda x: x['release_date'], reverse=True)

                    for actor_movie in sorted_actor_movies:
                        if len(movies) >= 4:
                            break

                        if actor_movie.get('poster_path'):
                            actor_movie_image_url = 'https://image.tmdb.org/t/p/w200'
                            actor_movie['poster_path'] = actor_movie_image_url + actor_movie['poster_path']
                            movie_posters.append(actor_movie)
                            movies.append(actor_movie['title'])

                    if movies:
                        person_name = person['name']
                        is_check = False
                        for cast in movies_cast:
                            if cast['person_name'] == person_name:
                                is_check = True
                                break

                        if not is_check:
                            movies_cast.append({
                                'person_name': person_name,
                                'movies': movies,
                            })

    # 최신순 정렬
    sorted_movies = sorted(movie_search_data['results'], key=lambda x: x['release_date'], reverse=True)

    # 페이지네이션
    page = request.GET.get('page', '1')
    per_page = 12
    paginator = Paginator(sorted_movies, per_page)
    posts = paginator.get_page(page)

    # 장르
    genre_dict = {
        28: '액션',
        12: '모험',
        16: '애니메이션',
        35: '코미디',
        80: '범죄',
        99: '다큐멘터리',
        18: '드라마',
        10751: '가족',
        14: '판타지',
        36: '역사',
        27: '공포',
        10402: '음악',
        9648: '미스터리',
        10749: '로맨스',
        878: 'SF',
        10770: 'TV 영화',
        53: '스릴러',
        10752: '전쟁',
        37: '서부'
    }

    context = {
        'movie_search_data': movie_search_data,
        'person_search_data': person_search_data,
        'posts': posts,
        'movies': movies,
        'query': query,
        'movies_cast': movies_cast,
        'movie_posters': movie_posters,
        'genre_dict': genre_dict,
    }

    return render(request, 'posts/search.html', context)


# 영화 상세정보와 그 영화에 쓰인 후기글을 보여줌
def movie_detail(request, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(url)
    movie_data = response.json()

    # 필요한 영화 정보 추출
    title = movie_data.get('title')
    overview = movie_data.get('overview')
    # release_date = movie_data.get('release_date')
    poster_path = movie_data.get('poster_path')
    if poster_path:
        poster_path = 'https://image.tmdb.org/t/p/w500' + movie_data.get('poster_path')

    genres = movie_data.get('genres', [])

    # 해당 영화에 쓰인 후기글 가져오기
    reviews = Post.objects.filter(movie_id=movie_id)

    # 영화의 한국 기준 개봉일자를 불러옵니다.
    release_dates_url = f'https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={TMDB_API_KEY}'
    release_dates_response = requests.get(release_dates_url)
    release_data = release_dates_response.json()

    for data in release_data['results']:
        if data["iso_3166_1"] == "KR":
            release_date = data["release_dates"][-1].get("release_date")
            break
    else:
        release_date = ''

    # 영화의 cast 정보(5명)가 credits에 저장되어 있습니다.
    # 템플릿에서는 for문을 사용하셔서 한 명씩 정보를 불러와 사용하시면 됩니다.
    # 배우 이름은 credits.name, 역할(캐릭터) 이름은 credits.character로 불러오시면 됩니다.
    credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-kr'
    credits_response = requests.get(credits_url)
    credits_data = credits_response.json()
    credits = credits_data['cast'][:6]
    profile_path = 'https://image.tmdb.org/t/p/w200'

    context = {
        'movie_id': movie_id,
        'title': title,
        'overview': overview,
        'release_date': release_date[:10],
        'poster_path': poster_path,
        'reviews': reviews,
        'genres': genres,
        'credits': credits,
        'profile_path': profile_path,
    }


    return render(request, 'posts/movie_detail.html', context)



def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post,
        'form': CommentForm()
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def create(request, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(url)
    movie_data = response.json()

    poster_path = 'https://image.tmdb.org/t/p/w200' + movie_data.get('poster_path')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.movie_id = movie_id
            post.user = request.user
            post.poster_path = poster_path
            post.movie_title = movie_data.get('title')
            post.movie_overview = movie_data.get('overview')
            post.movie_release_date = movie_data.get('release_date')
            score = float(request.POST['score'])
            post.score = score
            post.save()
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
        'movie': movie_data,
    }
    return render(request, 'posts/create.html', context)


@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                score = float(request.POST['score'])
                post.score = score
                post.save()
                return redirect('posts:post_detail', post.pk)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/update.html', context)


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    movie_id = post.movie_id
    if request.user == post.user:
        post.delete()
        return redirect('posts:movie_detail', movie_id)


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
    comment = Comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('posts:post_detail', post_pk)