from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=50)
    u_icon = models.ImageField(upload_to='icons/%Y-%m')

    objects = models.Manager()

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'UserModel'
        verbose_name_plural = 'UserModels'
