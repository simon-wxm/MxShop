# coding = utf-8
__author__ = 'wxm-simon'
from rest_framework import serializers
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from goods.models import Goods


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ('goods','nums')


class ShopCartSerilizer(serializers.Serializer):
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

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += 1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=True)
    class Meta:
        model =OrderInfo
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号
        from random import Random
        import time
        random_ins = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(time_str=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                       userid=self.context['request'].user.id,
                                                       ranstr = random_ins.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'