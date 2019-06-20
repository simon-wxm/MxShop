# coding = utf-8
__author__ = 'wxm-simon'
import xadmin
from .models import ShoppingCart,OrderInfo,OrderGoods

class ShoppingCardAdmin(object):
    list_display = ['user','goods','nums']


class OrderInfoAdmin(object):
    list_display = ['user','order_sn','tarde_no','pay_status','post_script','order_mount','pay_time','add_time']

    class OrderGoodsInline(object):
        model = OrderGoods
        exclude = ['add_time']
        extra = 1
        style = 'tab'
    inlines = [OrderGoodsInline,]

xadmin.site.register(ShoppingCart,ShoppingCardAdmin)
xadmin.site.register(OrderInfo,OrderInfoAdmin)

