from django.contrib import admin

from .models import Category, Genre, GenreTitle, Review, Title


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'get_genre', 'category', 'description'
    )
    inlines = [GenreTitleInline, ]
    list_filter = ('category', )
    list_display_links = ('name', )
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        return ', '.join((p.name for p in obj.genre.all()))


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('name', )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    list_fields = ('text', 'author__username')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
