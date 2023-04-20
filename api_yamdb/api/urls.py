from django.urls import include, path
from api.v1 import urls

app_name = 'api'

urlpatterns = [
    path('v1/', include(urls)),
]
