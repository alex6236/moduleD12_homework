from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    
    class Meta:
        model = Post
        fields = {
            'dataCreation': ['gt'], 
            'title': ['iregex'], 
            'author__authorUser__username': ['iregex'],
            'text': ['iregex'],
        }
        # fields = ('dataCreation', 'title', 'author__authorUser__username')