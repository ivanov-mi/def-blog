from django.db.models import Q, Count
from django_filters import rest_framework
from .models import Post

class PostFilter(rest_framework.FilterSet):
    hashtag = rest_framework.CharFilter(field_name='hashtags__name', lookup_expr='iexact')
    hot = rest_framework.BooleanFilter(method='filter_hot')

    def filter_hot(self, queryset, _, value):
        if value:
            hot_posts = queryset.annotate(
                comments_count=Count('comments'),
                likes_count=Count('votes', filter=Q(votes__is_liked=True)),
            ).filter(
                comments_count__gte=2,
                likes_count__gte=5,
            )
            return hot_posts

        return queryset

    class Meta:
        model = Post
        fields = ['hashtag', 'hot']