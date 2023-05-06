import requests

# 실시간 인기 영화 검색어
def trending_movies(request):
    TMDB_API_KEY = 'caea966f6e10b1fbcfc446cd0052d5cd' 

    trending_url = 'https://api.themoviedb.org/3/trending/movie/day'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ko-kr',
        'region': 'kr'
    }

    trending_response = requests.get(trending_url, params=params)
    trending_data = trending_response.json()
    trending = trending_data['results'][:10]

    return {'trending': trending,}

def genre_dict(request):
    return {'genre_dict': genre_dict}