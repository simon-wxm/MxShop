# coding = utf-8
__author__ = 'wxm-simon'
from rest_framework import serializers
from trade.models import ShoppingCart ,OrderInfo,OrderGoods
from goods.serializers import GoodsSerializers
from goods.models import Goods
"""


class ShopCartDetailSerializers(serializers.ModelSerializer):
    goods = GoodsSerializers(many=False,read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ('goods','nums')


class ShopCartSerilizers(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault() )
    nums = serializers.IntegerField(required=True,label='数量',min_value=1,error_messages={
        'min_value':'商品数量不能小于1',
        'required':'请选择购买数量'
    })
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user,goods=goods)
        if existed:
            existed = existed[0]
            existed.num += 1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializers(serializers.ModelSerializer):
    goods = GoodsSerializers(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'

# class OrderDetailSerializers(serializers.ModelSerializer):
#     goods = GoodsSerializers(many=True)
#     alipy_pay = serializers.SerializerMethodField(read_only=True)



"""