import sys,os
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+ "../")
# db_tools/import_category_data.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"MxShop.settings")

import django
django.setup()
from goods.models import GoodsCategory
from db_tools.data.category_data import row_data
# 添加一级类
for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat['code']
    lev1_intance.name = lev1_cat['name']
    lev1_intance.category_type = 1  # 一级类
    lev1_intance.save()
    #添加二级类
    for lev2_cat in lev1_cat['sub_categorys']:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat['code']
        lev2_intance.name = lev2_cat['name']
        lev2_intance.category_type = 2
        lev2_intance.parent_type = lev1_intance
        lev2_intance.save()
        # 添加三级类
        for lev3_cat in lev2_cat['sub_categorys']:
            lev3_intence = GoodsCategory()
            lev3_intence.code = lev3_cat['code']
            lev3_intence.name = lev3_cat['name']
            lev3_intence.category_type = 3
            lev3_intence.parent_type = lev2_intance
            lev3_intence.save()



# python  manage.py runscript import_category_data.py