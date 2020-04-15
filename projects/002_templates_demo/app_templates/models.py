from django.db import models

# Create your models here.


class Student(models.Model):
    s_name = models.CharField(max_length=10)
    s_age = models.IntegerField(default=20)

    def get_info(self):
        return f'{self.s_name}: {self.s_age}. by method'
