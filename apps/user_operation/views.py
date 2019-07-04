from django.shortcuts import render

# Create your views here.

from .models import UserFav
from .serializers import UserFavSerialiazer ,UserFavDetailSerializer
from rest_framework import  viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    '''
    用户收藏
    '''
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerialiazer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerialiazer

        return UserFavSerialiazer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

from .serializers import LeavingMessageSerializer
from .models import UserLeavingMessage
class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list: 获取用户的留言
    create: 添加留言
    delete: 删除留言
    """
    permission_classes = (IsAuthenticated ,IsOwnerOrReadOnly )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

from .serializers import UserAddressSerializer
from .models import UserAddress
class UserAddressViewset(viewsets.ModelViewSet):
    '''
    管理收货地址
    list:获取收获地址
    create:创建新的收货地址
    update:修改收货地址
    delete:删除收货地址
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


