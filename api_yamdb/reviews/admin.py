from django.contrib import admin

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_filter = ('genre', 'category')
    list_editable