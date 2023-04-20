import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter()
    year__gt = django_filters.NumberFilter(field_name='year', lookup_expr='gt')
    year__lt = django_filters.NumberFilter(field_name='year', lookup_expr='lt')

    name = django_filters.CharFilter()

    category = django_filters.CharFilter(lookup_expr='slug__iexact')
    genre = django_filters.CharFilter(lookup_expr='slug__iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
