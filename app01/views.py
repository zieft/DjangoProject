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


from django.core.validators import RegexValidator
from django.core.validators import ValidationError


class PrettyNumModelForm(forms.ModelForm):
    # # 字段验证，方法1：
    # mobile = forms.CharField(
    #     label='手机号',
    #     # validators=[RegexValidator(r'^159[0-9]+$', '号码必须以159开头')]
    #     validators=[RegexValidator(r'^1\d{10}$', '号码必须以1开头，总长度为11。')]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class='form-control'样式
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 字段验证，方法2：（钩子方法，可以进行重复号码的验证）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']  # 获取用户输入的数据
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        # 验证不通过，则抛出异常
        if len(txt_mobile) != 11:
            raise ValidationError('格式错误')
        elif exists:
            raise ValidationError('号码已存在')

        # 验证通过，返回用户输入的值
        return txt_mobile


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


class PrettyNumEditForm(forms.ModelForm):
    # 使字段不可更改：
    mobile = forms.CharField(
        disabled=True,
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加class='form-control'样式
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 字段验证，方法2：（钩子方法，可以进行重复号码的验证）（需要排除自己）
    def clean_mobile(self):
        current_id = self.instance.pk  # 获取当前实例的id
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=current_id).filter(mobile=txt_mobile).exists()
        # 验证不通过，则抛出异常
        if len(txt_mobile) != 11:
            raise ValidationError('格式错误')
        elif exists:
            raise ValidationError('号码已存在')

        # 验证通过，返回用户输入的值
        return txt_mobile


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
