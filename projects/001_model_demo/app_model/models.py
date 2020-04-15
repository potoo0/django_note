from django.db import models


# Create your models here.


class Grade(models.Model):
    ''' 班级数据表
    字段定义：
        id: 整数，自增长：主键（模型自动生成）
        g_name: 字符串，最大长度10：班级名称
    '''
    g_name = models.CharField(max_length=10)


class StudentManager(models.Manager):
    ''' 重写数据库查询方法，结果不返回 is_delete 为 True 的数据 '''
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(is_delete=False)

    def create_stu(self, s_name='Rick', s_age=18, s_grade_id=1):
        # 重写创建数据的方法
        stu = self.model()
        stu.s_name = s_name
        stu.s_age = s_age
        stu.s_grade_id = s_grade_id

        return stu


class Student(models.Model):
    ''' 学生信息数据表
    字段：
        s_name: 字符串，最大长度 10：学生姓名
        s_age: 整数，默认 20：学生年龄
        s_grade: 整数：学生班级（外连班级数据表）
        is_delete: 布尔，默认 False：逻辑删除
    '''
    s_name = models.CharField(max_length=10, blank=False)
    s_age = models.IntegerField(default=20)
    s_grade = models.ForeignKey(Grade)
    is_delete = models.BooleanField(default=False)

    objects = StudentManager()  # 重写查询方法

    @classmethod
    def create(cls, s_name='Rick', s_age=18, s_grade_id=1):
        return cls(s_name=s_name, s_age=s_age, s_grade_id=s_grade_id)

    def delete(self, using=None, keep_parents=False):
        ''' 重写数据库删除方法，实现逻辑删除 '''
        self.is_delete = True
        self.save()

    class Meta:
        ordering = ['-id']
        # db_table = ''
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'


class dateDemo(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    datetime = models.DateTimeField(auto_now=True)
