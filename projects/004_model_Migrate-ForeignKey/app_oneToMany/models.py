from django.db import models


class Grade(models.Model):
    g_name = models.CharField(max_length=10)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'


class Student(models.Model):
    s_name = models.CharField(max_length=10)
    s_age = models.IntegerField(default=20)
    s_grade = models.ForeignKey(
        Grade,
        null=True, blank=True,
        on_delete=models.PROTECT)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
