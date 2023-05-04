from django_filters import FilterSet
from .models import News


class NewsFilter(FilterSet):
    class Meta:
        model = News
        fields = {
            'date': ['icontains'],
            'header': ['icontains'],
            'description': ['icontains'],
            'cat': ['exact']
        }
