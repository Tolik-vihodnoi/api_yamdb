from django.urls import include, path
from .views import create_token, signup, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include([
        path('token/', create_token),
        path('signup/', signup)
    ]))
]