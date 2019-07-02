from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from .serializers import SmsSerializer
from rest_framework.response import Response
from MxShop.settings import APIKEY
from random import choice
from .models import  VerifyCode
from utils.yunpian import YunPian

User = get_user_model()

class CustomBackend(ModelBackend):
    '''自定义用户验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
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
        return ''.join(random_str)

    def create(self,request,*args,**kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        mobile = serializers.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code,mobile=mobile)

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