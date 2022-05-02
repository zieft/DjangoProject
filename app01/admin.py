from django.contrib import admin
from .models import UserInfo, PrettyNum, Department
# Register your models here.

# admin.site.register(UserInfo)
# admin.site.register(Department)
# admin.site.register(PrettyNum)
admin.site.site_header= '设备管理系统'
admin.site.site_title = '标签后'
admin.site.index_title = '主页'


class UserInfoManager(admin.ModelAdmin):
    list_display = ['name', 'gender', 'create_date', 'age']

admin.site.register(UserInfo, UserInfoManager)

class PrettyNumManager(admin.ModelAdmin):
    list_display = ['mobile', 'price', 'status', 'level']
    list_display_links = ['price']
    list_filter = ['level']
    search_fields = ['mobile']
    list_editable = ['level', 'status']
admin.site.register(PrettyNum, PrettyNumManager)
