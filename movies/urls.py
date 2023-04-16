from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'), # 단일 댓글 데이터 저장
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'), # 단일 댓글 데이터 삭제
    path('<int:movie_pk>/likes/', views.likes, name='likes'), # 단일 댓글 데이터 좋아요 및 좋아요 취소
    path('<int:hash_pk>/hashtag_filter/', views.hashtag_filter, name='hashtag_filter'),
]
