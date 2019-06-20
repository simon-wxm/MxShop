# coding = utf-8
import os,sys
pwd  = os.path.dirname(os.path.relpath(__file__))
sys.path.append(pwd+ '../')
from db_tools.data.product_data import row_data
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"MxShop.settings")

import django
django.setup()
from goods.models import Goods,GoodsCategoryBrand,GoodsImage,GoodsCategory

import re

for goods_detail in row_data:
    print('goods_detail',goods_detail['name'])
    goods = Goods()
    goods.name = goods_detail['name']
    goods.market_price = int(re.match(r".*?(\d+\.{0,}\d{0,}).*?", goods_detail['market_price']).group(1))
    goods.sale_price = int(re.match(r".*?(\d+\.{0,}\d{0,}).*?", goods_detail['sale_price']).group(1))
    goods.goods_brief = goods_detail['desc'] if  goods_detail['desc'] is not None  else ''
    goods.goods_desc = goods_detail['goods_desc'] if  goods_detail['goods_desc'] is not None else ''
    goods.goods_front_images = goods_detail['images'][0] if goods_detail['images'] else ''
    category_name = goods_detail['categorys'][-1]  # 最后一个最精确
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()
    # F:\test\MxShop\db_tools\import_category_data.py

    for goods_image in goods_detail['images']:
        goodsImage = GoodsImage()
        goodsImage.image = goods_image
        goodsImage.goods = goods
        goodsImage.save()
