from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('movie_detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('create/<int:movie_id>/', views.create, name='create'),
    path('<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:post_pk>/update', views.update, name='update'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/likes/', views.post_likes, name='post_likes'),
    path('<int:post_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/likes', views.comment_likes, name='comment_likes'),
]
