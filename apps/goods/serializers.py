# coding = utf-8
from rest_framework import serializers
from goods.models import Goods,GoodsImage,GoodsCategory,GoodsCategoryBrand
from goods.models import IndexAd,HotSearchWords,Banner
from django.db.models import Q


class CategorySerializers3(serializers.ModelSerializer):
    '''三级分类'''
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializers2(serializers.ModelSerializer):
    ''' 二级分类  '''
    sub_cat = CategorySerializers3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''一级分类'''
    sub_cat = CategorySerializers2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializers(serializers.ModelSerializer):
    '''轮播图'''
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    '''商品'''
    category = CategorySerializer()
    images = GoodsImageSerializers(many=True)
    class Meta:
        model = Goods
        fields = '__all__'


class BannerSerializers(serializers.ModelSerializer):
    '''轮播图'''
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializers(serializers.ModelSerializer):
    '''大分类下的宣传商标'''
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializers(serializers.ModelSerializer):
    brand  = BannerSerializers(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializers2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id,)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            # 在serializers 中嵌套使用,应该将本地的request传给嵌套的序列化使用
            goods_json = GoodsSerializer(goods_ins,many=True, context={'request':self.context['request']})
            # goods_json应该是一个序列化的信息, .data才是值
            return goods_json.data

    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id = obj.id) | Q(category__parent_category_id = obj.id) |
                                         Q(category__parent_category__parent_category_id = obj.id) )
        goods_serializers  = GoodsSerializer(all_goods, many=True, context={'request':self.context['request']})
        return  goods_serializers.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class HotWordSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords

