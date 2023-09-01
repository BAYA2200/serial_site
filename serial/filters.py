import django_filters
from .models import TVShow

class TVShowFilter(django_filters.FilterSet):
    class Meta:
        model = TVShow
        fields = {
            'genres': ['exact'],  # Filter for genres using exact match
        }
