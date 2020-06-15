from django.db import models


class Student(models.Model):
    s_name = models.CharField(max_length=50)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
