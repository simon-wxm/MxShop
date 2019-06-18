# coding= utf-8
__author__ = 'simon-wxm'
import xadmin
from xadmin import views
from .models import VerifyCode

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = '牛逼的应用'
    site_footer = "http://www.daxiongdi.com"
    #菜单收缩
    menu_style = 'accordion'

class VerifyCodeAdmin(object):
    list_display = ['code','mobile','add_time']


xadmin.site.register(VerifyCode,VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
