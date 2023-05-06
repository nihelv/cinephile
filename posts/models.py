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
    movie_overview = models.CharField(max_length=200)
    movie_release_date = models.CharField(max_length=200)



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    
    def get_movie_title(self):
        return self.post.movie_title