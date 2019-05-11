import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_ordering')

    class Meta:
        model = Post
        fields = ('title', 'created', 'author')
        # fields = {
        #     'title': ['icontains'],
        #     'created': ['iexact'],
        #     'author': ['iexact'],
        #     }
    
    def filter_by_ordering(self, queryset, name, value):
        if value == 'ascending':
            expression = 'created'
        elif value == 'descending':
            expression = '-created'

        return queryset.order_by(expression)