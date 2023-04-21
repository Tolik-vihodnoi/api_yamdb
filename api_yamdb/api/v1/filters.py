import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    category = django_filters.CharFilter(lookup_expr='slug__iexact')
    genre = django_filters.CharFilter(lookup_expr='slug__iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
