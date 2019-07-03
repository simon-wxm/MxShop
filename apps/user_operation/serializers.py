from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator


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

