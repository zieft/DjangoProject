from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError


class UserModelForm(BootStrapModelForm):
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


class PrettyNumModelForm(BootStrapModelForm):
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


class PrettyNumEditForm(BootStrapModelForm):
    # 使字段不可更改：
    mobile = forms.CharField(
        disabled=True,
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = '__all__'

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
