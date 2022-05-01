from django.db import models

# Create your models here.
class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)

    create_date = models.DateTimeField(verbose_name='入职时间')

    gender_choices = (
        (1, '男'),
        (0, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    # department_id = models.BigIntegerField(verbose_name="部门ID")
    depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="id", on_delete=models.CASCADE)
