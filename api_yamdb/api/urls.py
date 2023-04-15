from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, create_token, signup, \
    UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='user')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include([
        path('token/', create_token),
        path('signup/', signup)
    ]))
]