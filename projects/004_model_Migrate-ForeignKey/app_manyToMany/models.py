from django.db import models
from django.db.models.fields.related_descriptors import create_forward_many_to_many_manager


class Customer(models.Model):
    c_name = models.CharField(max_length=50)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Goods(models.Model):
    g_name = models.CharField(max_length=50)
    g_customer = models.ManyToManyField(Customer)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Goods'
        verbose_name_plural = 'Goodss'
