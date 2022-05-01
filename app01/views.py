from django.shortcuts import render, redirect
from app01 import models


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


from django import forms


class UserModelForm(forms.ModelForm):
    # 下面这行用于定义用户名的最小长度约束，可以用于validation
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", 'password', 'age', 'account', 'create_date', 'gender', 'depart']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }
    def __init__(self, *args, **kwargs):
        """
        重新定义__init__方法
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class='form-control'样式
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

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
    else: # 校验失败，在页面上显示错误信息
        print(form.errors)
        return render(request, 'user_add.html', {'form': form})

