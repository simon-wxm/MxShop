import  re
from datetime import  datetime, timedelta

from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self,mobile):
        '''手机号码验证'''
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        if not re.match(REGEX_MOBILE, mobile):
            raise  serializers.ValidationError('手机号码非法')

        one_mintes_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise  serializers.ValidationError('距离上一次发送时间未超过60秒')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误',
                                 }, help_text='验证码')
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all(), message='用户已经存在') ])

    password = serializers.CharField(style={'input_type':'password'}, label=True, write_only=True)

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            last_record = verify_records
            five_mintes_ago = datetime.now() - timedelta(minutes=5)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码已经过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')

        else:
             raise serializers.ValidationError('验证码错误')

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        field = ('username', 'code', 'mobile', 'password')




