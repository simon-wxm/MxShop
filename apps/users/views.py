from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status ,mixins
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .serializers import SmsSerializer
from rest_framework.response import Response
from MxShop.settings import APIKEY
from random import choice
from .models import  VerifyCode
from utils.yunpian import YunPian
from .serializers import UserRegSerializer, UserDetailSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication, permissions
User = get_user_model()

class CustomBackend(ModelBackend):
    '''自定义用户验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
            print('验证用户的信息', username , password )
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewsite(CreateModelMixin,viewsets.GenericViewSet):
    '''手机验证码'''
    serializer_class = SmsSerializer
    def generate_code(self):
        '''生成四位数的验证码'''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        print('生成的code ',''.join(random_str) )
        return ''.join(random_str)

    def create(self,request,*args,**kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        mobile = serializers.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        print('code _ views 002')
        sms_status = {'code':0,'msg':'验证码123' } # yun_pian.send_sms(code=code,mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'monile':sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                'mobile':mobile
            },status = status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet, mixins.DestroyModelMixin ):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        print( ' user ,payload, jwt_encode_handler(payload) 进行了什么操作 ',  user , payload , jwt_encode_handler(payload))
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []

        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer

        return UserDetailSerializer

    def get_object(self):
        return self.request.user





