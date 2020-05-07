from django.db import models


class Animal(models.Model):
    a_age = models.IntegerField(default=2)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'
        abstract = True


class Cat(Animal):
    c_name = models.CharField(max_length=50)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Cat'
        verbose_name_plural = 'Cats'


class Dog(Animal):
    d_name = models.CharField(max_length=50)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Dog'
        verbose_name_plural = 'Dogs'
