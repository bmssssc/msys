from datetime import datetime
from django.db import models, connection
from django.db import models
from pmapps.user.base_model import BaseModel


class EmployeeCodeAutoField(models.CharField):
    def get_db_prep_value(self, value, connection, prepared=False):
        cursor = connection.cursor()
        cursor.execute('select max(employee_code) from t_user')
        max_employee_code = cursor.fetchone()[0]
        cursor.close()
        if max_employee_code:
            max_employee_code = int(max_employee_code) + 1
            max_employee_code = '%07d' % max_employee_code
        else:
            max_employee_code = "%07d" % 1
        return max_employee_code


class User(BaseModel):
    employee_code = EmployeeCodeAutoField(max_length=20,
                                          editable=False,
                                          verbose_name='工号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    departments = (
        (0, '未选择'),
        (1, '开发部'),
        (2, '计划部'),
        (3, '财务部'),
        (4, '仓储部'),
        (5, '人力资源部'),
        (6, '生产部'),
        (7, '采购部'),
    )
    department = models.IntegerField(choices=departments,
                                     default=0,
                                     verbose_name='部门')
    account = models.CharField(max_length=20, verbose_name='账号')
    password = models.CharField(max_length=16, verbose_name='密码')
    email = models.CharField(max_length=20, null=True, blank=True, verbose_name='邮箱')
    phone = models.IntegerField(null=True, blank=True, verbose_name='手机')

    @property
    def department_name(self):
        return self.departments[self.department][1]

    def __str__(self):
        return '%s-%s' % (self.employee_code, self.name)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Material(BaseModel):
    code = models.IntegerField(verbose_name='编码')
    name = models.CharField(max_length=20, verbose_name='名称')
    categories = (
        (0, '未选择'),
        (1, '电子物料'),
        (2, '线材'),
        (3, '五金'),
        (4, '包材'),
        (5, '辅料'),
    )
    category = models.IntegerField(choices=categories,
                                   default=0,
                                   verbose_name='种类')
    info = models.CharField(max_length=200, verbose_name='描述')
    num = models.IntegerField(verbose_name='数量')

    @property
    def category_name(self):
        return self.categories[self.category][1]

    def __str__(self):
        return '%s-%s-%s' % (self.code, self.name, self.info)

    class Meta:
        db_table = 't_material'
        verbose_name = '物料信息表'
        verbose_name_plural = verbose_name


class OrderSnAutoField(models.CharField):
    def get_db_prep_value(self, value, connection, prepared=False):
        today = datetime.today().strftime('%Y%m%d')  # 20181207
        cursor = connection.cursor()

        cursor.execute('select max(order_sn) from t_order')
        max_order_sn = cursor.fetchone()[0]  # ('20181212000001',)  或 (None,)

        cursor.close()

        if max_order_sn:
            max_order_date = max_order_sn[:8]  # yyyymmdd
            if today == max_order_date:
                sn = str(int(max_order_sn[8:]) + 1)
                return today + sn.rjust(6, '0')

        return today + '000001'  # 今天的第一单


class RequiredList(BaseModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='物料')
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='申请人')
    num = models.IntegerField(verbose_name='需求数量')
    states = (
        (0, '申请中'),
        (1, '已审核'),
        (2, '备料中'),
        (3, '已回料'),
    )
    state = models.IntegerField(choices=states,
                                default=0,
                                verbose_name='物料状态')

    @property
    def states_name(self):
        return self.states[self.state][1]

    def __str__(self):
        return '%s' % self.material

    class Meta:
        db_table = 't_required_list'
        verbose_name = '需求物料清单表'
        verbose_name_plural = verbose_name


class Order(BaseModel):
    order_sn = OrderSnAutoField(max_length=20,
                                editable=False,
                                verbose_name='流水号')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='当前处理人')
    detail = models.ForeignKey(RequiredList, verbose_name='物料详情')

    content = models.CharField(max_length=100, verbose_name='申请用途')
    is_agree = models.BooleanField(default=False, verbose_name='是否同意')

    def __str__(self):
        return '%s因%s所需物料' % (self.user, self.content)

    class Meta:
        db_table = 't_order'
        verbose_name = '清单状态表'
        verbose_name_plural = verbose_name
