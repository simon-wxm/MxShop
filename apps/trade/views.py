from django.shortcuts import render

# Create your views here.
from .serializers import ShopCartDetailSerializer, ShopCartSerilizer, OrderDetailSerializer, OrderGoodsSerializer ,OrderSerializer
from .models import OrderGoods, ShoppingCart, OrderInfo
from rest_framework import viewsets, mixins

from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

class ShoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    list:获取购物车列表
    create:加入购物车
    delete:删除购物记录
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class =  ShopCartSerilizer
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return   ShopCartSerilizer


class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:获取个人订单
    delete: 删除订单
    create:新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication ,SessionAuthentication)
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order

