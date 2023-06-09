from django.contrib import admin
from django.db.models import Avg

from .models import Category, Genre, GenreTitle, Review, Title


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'genres',
        'rating', 'category', 'description'
    )
    inlines = [GenreTitleInline, ]
    list_filter = ('category', )
    list_display_links = ('name', )
    empty_value_display = '-пусто-'

    def genres(self, obj):
        return ', '.join((p.name for p in obj.genre.all()))

    def rating(self, obj):
        return round(obj.rating, 1)

    def get_queryset(self, request):
        return Title.objects.annotate(rating=Avg('reviews__score'))


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('name', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    list_fields = ('text', 'author__username')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
