from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import GoodsSerializer
from user_operation.models import UserLeavingMessage


class UserFavSerialiazer(serializers.ModelSerializer):
    # 获取到当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault() )
    print('user.username',user)
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        model = UserFav
        fields = ('user', 'goods', 'id')

class UserFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''
    # 通过商品id获取收藏的商品，需要嵌套商品的序列化
    goods = GoodsSerializer
    class Meta:
        model = UserFav
        fields = ('goods','id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    用户留言
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


from .models import UserAddress

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault() )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%D %H:%M:%S')

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'add_time')

