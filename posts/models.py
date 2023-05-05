from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    movie_title = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    poster_path = models.CharField(max_length=200)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    
    def get_movie_title(self):
        return self.post.movie_title
    
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