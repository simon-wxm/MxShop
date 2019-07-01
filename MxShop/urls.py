# coding=utf-8
from rest_framework_jwt.views import obtain_jwt_token

__author__ = 'wxm-simon'
# from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.static import serve
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from goods.views import CategoryViewSet
from rest_framework.authtoken import views
router = DefaultRouter()

router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet, base_name='categorys')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('docs', include_docs_urls(title='牛逼的应用')),
    re_path('^', include(router.urls)),
    path('api-token-auth/',views.obtain_auth_token),
    path('login/', obtain_jwt_token),
]
