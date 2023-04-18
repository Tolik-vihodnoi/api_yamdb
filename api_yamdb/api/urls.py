from django.urls import include, path
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    create_token, signup, UserViewSet, CommentViewSet,
                    ReviewViewSet)
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='user')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include([
        path('token/', create_token),
        path('signup/', signup)
    ]))
]
