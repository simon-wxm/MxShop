from django.shortcuts import render

# Create your views here.

from .models import UserFav
from .serializers import UserFavSerialiazer
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

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)






