from django.contrib import admin
from .models import TVShow, Genre, Episode, Comment


class TVShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('genres',)  # Добавляем жанры как виджет выбора множества значений


admin.site.register(TVShow, TVShowAdmin)
admin.site.register(Genre)
admin.site.register(Episode,)
admin.site.register(Comment)

