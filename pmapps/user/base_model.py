from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注')

    class Meta:
        abstract = True
