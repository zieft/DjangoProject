from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.form import *


# Create your views here.

def depart_list(request):
    # queryset可以理解为列表，里面存放的都是对象[对象，对象，对象]，每个对象里封装着一行数据
    # 这个set在后端循环没有意义，在前端循环更有意义
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    # 按下“新建部门”按钮后，跳转页面
    if request.method == 'GET':
        return render(request, 'depart_add.html', )

    # 在新建部门页面 按下提交按键，获取post提交过来的数据
    title = request.POST.get('title')

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回到部门列表页面
    return redirect("/depart/list/")


def depart_delete(request):
    # 获取id
    nid = request.GET.get('nid')
    # 执行删除
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    if request.method == 'GET':
        # 根据nid获取数据
        # models.Department.objects.filter(id=nid)获得的是个queryset [obj,]，需要.first()来获取里面的元素obj
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})

    # 获取用户提交的更改后的部门名称
    new_title = request.POST.get('title')
    # 更新
    models.Department.objects.filter(id=nid).update(title=new_title)
    # 跳转回部门列表页面
    return redirect("/depart/list/")


def user_list(request):
    # 获取所有用户列表
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     # 用python语法获取数据
    #     # 获取日期的字符串形式
    #     obj.create_date.strftime("%Y-%m-%d")
    #     # 获取性别代号，和性别
    #     obj.gender # 这样获取的是性别的代号，1或者0
    #     obj.get_gender_display() # 这样就是直接获取男或者女
    #     #获取部门id，和部门名称
    #     obj.depart_id # 部门id
    #     obj.depart.title # obj.depart直接获取Department表的一行，这个关联在models.py中定义
    #     # 但是在前端中获取这些信息更合理
    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})

    # POST提交的数据，数据进行校验、
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    else:  # 校验失败，在页面上显示错误信息
        print(form.errors)
        return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    if request.method == 'GET':
        # 根据ID从数据库获取要编辑的那一行数据
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


from django.utils.safestring import mark_safe  # 用于标记从后端传到前端的字符串为安全的，从而可以转换成html


###  以下是靓号管理
def num_list(request):
    total_count = models.PrettyNum.objects.all().count()
    page = int(request.GET.get('page', 1))
    page_size = 10
    total_page_numbers, rest = divmod(total_count, page_size)
    if rest:
        total_page_numbers += 1
    start = (page - 1) * page_size
    end = page * page_size
    # -level: 按级别倒序排列
    queryset = models.PrettyNum.objects.all().order_by('-level')[start:end]

    # 页码
    page_str_list = []
    for i in range(1, total_page_numbers + 1):
        ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    page_str = mark_safe("".join(page_str_list))  # 不加mark_safe的话，前端无法将此字符串转换成html代码
    return render(request, 'num_list.html', {'queryset': queryset, 'page_str': page_str})


def num_add(request):
    if request.method == 'GET':
        form = PrettyNumModelForm()
        return render(request, 'num_add.html', {'form': form})
    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    else:
        return render(request, 'num_add.html', {'form': form})


def num_edit(request, nid):
    if request.method == 'GET':
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyNumEditForm(instance=row_object)
        return render(request, 'num_edit.html', {'form': form})
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyNumEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    else:
        return render(request, 'num_edit.html', {'form': form})


def num_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/num/list/')


def num_createalot(request):
    for i in range(300):
        models.PrettyNum.objects.create(mobile=str(15928431617 + i), price=300)

    return redirect('/num/list/')


from app01.utils.pagination import Pagination
def member_list(request):
    """
    非组内用户列表
    :param request:
    :return:
    """
    queryset = models.Member.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        'queryset':queryset,
        'page_string': page_object.html(),
    }
    return render(request, 'member_list.html', context)



from app01.utils.encrypt import md5
class MemberModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput, # model里没定义的表单，widget必须写在这里
                                    # 输错密码后，默认清空输入框，如果不想清空可以 forms.PasswordInput(render_value=True)

    )

    class Meta:
        model = models.Member
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput,
            'confirm_password': forms.PasswordInput, # 在此类里新定义的表单，不行。这里只影响model里定义的表单

        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))

        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')
        return confirm # 这里return什么值，下面form.save()数据库里就保存什么值


def member_add(request):
    title = "添加非组内用户"

    if request.method == 'GET':
        form = MemberModelForm
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'template_add.html', context)

    form = MemberModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/member/list/')
    else:
        return render(request, 'template_add.html', {'form': form, 'title': '添加非组内用户'})
