import xadmin as admin
from pmapps.user.models import *
from xadmin import views


class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


admin.site.register(views.BaseAdminView, BaseSetting)


class UserAdmin:
    list_display = ['employee_code', 'name', 'department', 'email', 'phone', 'created', 'updated']
    search_fields = ['employee_code', 'name', 'email', 'phone', ]
    list_per_page = 10


class MaterialAdmin:
    list_display = ['code', 'name', 'category', 'info', 'num', 'created', 'updated']
    search_fields = ['code', 'name', 'info']
    list_per_page = 10


class RequireListAdmin:
    list_display = ['material', 'person', 'state']
    search_fields = ['material', ]
    list_per_page = 10


class OrderAdmin:
    list_display = ['order_sn', 'user', 'detail', 'content', 'is_agree']
    search_fields = ['order_sn', 'user']
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(RequiredList, RequireListAdmin)
admin.site.register(Order, OrderAdmin)
