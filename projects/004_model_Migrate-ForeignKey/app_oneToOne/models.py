from django.db import models


class Person(models.Model):
    p_name = models.CharField(max_length=16)
    p_sex = models.BooleanField(default=False)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'


class IDcard(models.Model):
    id_num = models.CharField(max_length=18, unique=True)
    id_person = models.OneToOneField(
        Person,
        null=True, blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'IDcard'
        verbose_name_plural = 'IDcards'
