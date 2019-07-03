from django.shortcuts import render

# Create your views here.

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerializers
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

class GoodsPagination(PageNumberPagination):
    '''商品列表自定义分页'''
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class GoodsListViewSet(generics.ListAPIView, viewsets.GenericViewSet, mixins.RetrieveModelMixin ):
    '''商品列表页'''
    queryset = Goods.objects.all().order_by('id')
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializers
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter )

    filter_class = GoodsFilter

    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

from  rest_framework import mixins
from goods.serializers import CategorySerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list: 商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

# return axios.get(`${local_host}/categorys/`+params.id+'/');


