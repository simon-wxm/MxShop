import django_filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(name='category',method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        return queryset.filter(Q(categoyr_id = value) | Q(category__parent_category=value)
                               | Q(category__parent_category__parent_category = value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']

