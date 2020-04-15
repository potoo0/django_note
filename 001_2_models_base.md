《千峰教育 django 视频教程》的学习笔记。

---

django 中已经集成 ORM，故 model 操作数据库时直接调 Python 函数即可，不需要写 SQL。

导入 ORM 操作的父类 models：

```python
from django.db import models
```

模型相关的学习和测试推荐在项目命令行中进行：

```python
python manage.py shell
```

## 1. 概述

- django 会根据属性的类型确定下面信息：
  - 根据当前数据库种类确定支持的字段类型
  - 渲染管理表单时使用的默认 html 控件
  - 在管理站点最低限度的验证
- django 会为表增加自动增长的主键(字段名为 id)，每个模型只能有一个，如果使用参数 primary_key 设置某属性为主键后，则 django 不会再生成主键
- 属性命令限制：除标识符规则外，django 要求不允许使用连续的下划线(查询规则占用)。
- 删除支持逻辑删除，不做物理删除(常用于重要数据)，通过定义 isDelete 属性，默认 False 的 BooleanField 类型。

## 2. 模型定义

一个模型类在数据库中对应一张表，模型类中定义的属性，对应数据表中的一个字段。

### 2.1 模型类定义

定义 Python 的类，再继承 `models.Model` 即可。

### 2.2 属性定义

使用下面的字段函数在模型类中定义属性即可。

- `AutoField`: 一个根据实际 ID 自增长的 IntegerField，通常不指定。如果不指定，模型会自动添加主键;
- `CharField(max_length)`: 字符串，默认的表单样式是 TextInput;
- `TextField`: 大文本字符串，默认表单是 Textarea;
- `IntegerField`: 整数;
- `DecimalField(max_digits=None, decimal_place=None)`: 使用 Python 的 decimal.Decimal 实例表示十进制浮点数（优点是高精度）。其中 max_digits: 位数总数，decimal_place: 小数点后数字位数;
- `FloatField`: 使用 Python 的 float 实例表示的浮点数;
- `BooleanField`: true/false，默认表单控制是 CheckboxInput;
- `NullBooleanField`: null/true/false;
- `DateField(auto_now=False, auto_now_add=False)`: 使用 Python 的 datetime.date 实例表示的日期（年月日）。其中 auto_now: 每次保存时自动设置日期为当前日期，auto_now_add: 创建对象时自动设置为当前时间。默认表单控件为 TextInput;
- `TimeField`: 使用 Python 的 datetime.time 实例表示的时间（时分秒.微秒）。参数同上;
- `DateTimeField`: 使用 Python 的 datetime.datetime 实例表示的日期和时间（年月日-时分秒.微秒）。参数同上;
- `FileField`: 文件(能存，但没有必要);
- `ImageField`: 继承 FileField 的所有属性和方法，但加了对对象是否为图片的校验(能存，但没有必要)。

对于上面属性可通过一些选项来约束字段，如：

- `null=False`: 若为 True，则将允许空值以 NULL 存入数据库中。相当于 Python 的 `None`;
- `blank=False`: 若为 True，则此字段允许空白。相当于 Python 的 空字符串`''`;
- `db_colunm`: 字段的名称，如果未指定则使用属性名;
- `db_index`: 若为 True，则在数据表中为此字段创建索引;
- `default`: 此字段数据的默认值;
- `primary_key=False`: 若为 True，则该字段会成为模型的主键;
- `unique`: 若为 True，则该字段的在表中具有唯一值;
- `help_text`: 在表单 form 中显示此帮助文本。

---

外键：

外键作用：一张表的外键是另一张表的主键。作用是用来和其他表建立联系。如一张表记录了学生，另一张表记录了班级，而每个学生可能属于不同班级，则学生的数据表与班级数据表就产生了关联，称这种关系为外键。

外键分类：

- `ForeignKey`: 一对多。如：一张学生表与一张班级表，学生可能属于不同班级，学生表建立此外键来关联班级表;
- `OneToOneField`: 一对一;
- `ManyToManyField`: 多对多。

### 2.3 元选项

在模型类中定义 Meta，用于设置元信息，如：

```python
class Meta:
    db_table = 'ModelName'  # 数据表表名
    ordering = ['id', '-age', '?date']  # 查询的返回结果按 id 字段升序、age 降序、date 随机排序
```

此部分模型类定义如：

```python
class Grade(models.Model):
    g_name = models.CharField(max_length=10)


class Student(models.Model):
    s_name = models.CharField(max_length=10, blank=False)
    s_age = models.IntegerField(default=20)
    s_grade = models.ForeignKey(Grade)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        # db_table = ''
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'


class dateDemo(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    datetime = models.DateTimeField(auto_now=True)
```

## 3. 数据库操作

### 3.1 简单操作

导入定义 Model 并实例化后，简单的增删改查(CRUD)如下:

- 增: 为各字段赋值，`save` 方法完成保存；
- 查: 查所有: `all` 方法；查单个: `get()`，如按主键: `get(pk=x)`，按age字段：`get(age=x)`；
- 删: 基于查询，`delete` 方法完成删除；
- 改: 基于查询，更改数据后，`save` 方法完成保存。

> pk 为主键的快捷

### 3.2 模型数据插入

可以在模型实例化时传入关键字参数，或使用模型管理器 objects 的 create 方法来增加，将各字段的值作为关键字参数传入。如：

```python
from app_model.models import Grade, Student, dateDemo

# 1. 关联表插入数据
for index in range(1, 3):
    g = Grade.objects.create(g_name=f'g_{index:03}')
    g.save()
# 2.1 简单插入：先实例化再赋值。
s1 = Student()
s1.s_name = 'Rick_001'
s1.s_grade_id = 1
s1.save()
# 2.2 实例化时传入关键字参数
s2 = Student(s_name='Rick_002', s_grade_id=2)
s2.save()
# 2.3 模型管理器的 create 方法，传入关键字参数
s3 = Student.objects.create(s_name='Rick_003', s_grade_id=1)
s3.save()

# 2.3在创建对象时未指定 s_grade_id，会引发不能为空的错误
s4 = Student.objects.create(s_name='Rick_004', s_age=18)

```

模型管理器的 create 方法弊端是如果有某个字段在构建时未指定默认值，又未传入值，则会导致该字段为空或者引发不能为空的错误。故可以使用下面的自定义插入数据的方法：由于 `__init__` 在父类 models.Model 已经使用，因此在模型类中新建类方法(classmethod)来创建 create 函数：

```python
class Student(models.Model):

    # 字段声明、元选项同上

    @classmethod
    def create(cls, s_name='Rick', s_age=18, s_grade_id=1):
        return cls(s_name=s_name, s_age=s_age, s_grade_id=s_grade_id)

```

在插入数据时调 `Student.create()` 即可，这样也可以支持位置传参。如：

```python
s5 = Student.create('Rick_005')
s5.save()
```

### 3.3 模型数据查询

#### 3.3.1 获取查询集

管理器 objects 调用方法返回查询集，常用查询方法和过滤器有：

- `all()`: 返回所有数据
- `filter()`:  返回满足筛选条件的结果
- `exclude()`: 返回不满足筛选条件的结果
- `order_by()`: 排序，默认是 id，'-id'表示倒序
- `values()`: 返回一个查询集，每条数据是一个字典

实际上管理器 objects 的这几种查询返回的查询集都是 `models.query.QuerySet` 类型，此类型均可链式使用上面的五种方法，且 `QuerySet` 是 懒加载 的方式，并支持迭代和“切片”（与 Python 的切片不同）操作。

> 查询集的索引：使用类似“切片”的操作 - 使用下标来查指定范围的数据，相当于 sql 的 offset 与 limit。其与 python 的切片不同是其不会创建对象的拷贝。
> 查询集的缓存：每个查询集都包含一个缓存，来最小化对数据库的访问。新建查询集时缓存首次为空，第一次对缓存集求值发生数据缓存，以后的查询集使用缓存。  

如：

```python
# 构造数据，在上面自己创建的 create 函数基础上
for index in range(6, 16):
    student = Student.create(f'Rick_{index:03}', index)
    student.save()
# .all 查询
students_all = Student.objects.all()
print(type(students_all))
#students_fe = students_all.filter(s_age__gt=8).exclude(s_age__gt=12)
# 过滤器条件查询
students = Student.objects.filter(s_age__gt=8).exclude(s_age__gt=12)
print(type(students))
# students_fe 与 students 完全相同

# 迭代
for stu in students:
    print(f'name: {stu.s_name}, age: {stu.s_age}')
# 切片
print(students[1].s_name, students[1].s_age)
# 使用 values 转字典
print(students.values())
```

##### 查询条件

规则：属性\__运算符=值
运算符：

- exact: 判断，大小写敏感。如: `filter(name__exact='Rick')`
- contains: 是否包含，大小写敏感。如: `name__contains='Ric'`
- startswith, endswith: 以xx开头、结尾，大小写敏感。如: `name__startswith='Ri'`
- 以上四个在运算符前加 `i`，则不再区分大小写，如 `name__icontains='ri'`
- isnull, isnotnull: 是否为空。如 `name__isnull=False`
- in: 是否包含在给定数据内。如 `pk__in=[1, 3, 30]`
- gt, lt, gte, lte: 大于、小于、大于等于、小于等于

时间的查询规则：属性\__时间单位=值
时间单位：year, month, day, week_day, hour, minute, second. 如: `filter(datetime__month=2)`

但是 django 中时间条件查询有时区问题，会干扰对时间的正确筛选，解决方案有两种：

- 关闭 django 的自定义时区：更改 settings 的 `USE_TZ` 为 False
- 在数据库中创建对应的时区表（较麻烦，不推荐）

跨关系查询：
规则：模型类名\__属性名__比较运算符（实际上就是数据库中的 join）。
如 查询名字中带有"ric"的数据属于哪个班级(模型类名小写)：

```python
grade = Grade.objects.filter(student__s_name__icontains='ric')
```

#### 3.3.2 获取单个数据

- `get()`: 在模型管理器上获取单个数据。若没有找到符合对象，则引发 *DoesNotExist*；若找到多个，则引发 *MultipleObjectsReturned* 。错误捕获见下
- `first()`: 返回查询集的第一个对象
- `last()`: 返回查询集的最后一个对象
- `count()`: 返回查询集对象的个数
- `exists()`: 查询集是否为空

> get 的两种错误捕获：
>
> - 使用模型类捕获：modelname.DoesNotExist/MultipleObjectsReturned
> - django.core.exceptions.ObjectDoesNotExist/MultipleObjectsReturned

如：

```python
# get 查单条
student = Student.objects.get(pk=1)
print(student.pk, student.s_name)

# get 没找到符合的对象
try:
    student = Student.objects.get(pk=99)
except Student.DoesNotExist:
    print('不存在')
# get 查到多个符合对象
try:
    student = Student.objects.get(s_age=20)
except Student.MultipleObjectsReturned:
    print('查到多个符合对象')

# first
students = Student.objects.all()
print(students.first().s_name)

# count, exists
students = Student.objects.all()
print(students.count(), students.exists())

students = Student.objects.filter(s_age__gt=50)
print(students.count(), students.exists())
```

#### 3.3.3 聚合函数

聚合函数是对列进行求和、平均等简单的统计，输入参数是列名。

django 中使用 aggregate() 返回聚合函数的值（返回值为字典），聚合函数从 models 中导入，聚合函数有：`Avg`, `Count`, `Max`, `Min`, `Sum`。

如：

```python
from django.db.models import Max

max_age = Student.objects.aggregate(Max('s_age'))
print(max_age)
```

### 3.4 复杂查询 -- F对象与 Q对象

F 对象：使用模型的 A 属性与 B属性进行比较，且支持算术运算符。

如：

```python
from django.db.models import F

# 获取 student 中 age 大于 id 的数据
student = Student.objects.filter(s_age__gt=F('id') * 10)
print(student.values())
```

Q 对象：过滤器方法中的关键参数，常用于组合条件（避免过滤器过多地链式调用），支持 |(or), &(and), ~(not)。

如：

```python
from django.db.models import Q

students = Student.objects.filter(Q(s_age__gt=8) & ~Q(s_age__gt=12))
print(students.values())
```

## 4. 模型属性

模型属性：

- 显性属性：手动定义的属性
- 隐性属性：objects，模型管理器，是一个 Manager 类型的一个对象，用于数据库交互。当模型没有指定管理器时，django 会自动创建。

自定义模型管理器，新建类继承 models.Manager，在模型类中实例化。如实现 逻辑删除 和模型管理器中重写 create 函数：

```python
class StudentManager(models.Manager):
    def get_queryset(self):
        # 检查 is_delete 字段，判断过滤掉逻辑删除的数据
        return super(StudentManager, self).get_queryset().filter(is_delete=False)

    def create_stu(self, s_name='Rick'):
        # 重写创建数据的方法
        stu = self.model()
        stu.s_name = s_name

        return stu


class Student(models.Model):
    s_name = models.CharField(max_length=10)
    is_delete = models.BooleanField(default=False)

    objects = StudentManager()  # 重写查询方法

    def delete(self, using=None, keep_parents=False):
        ''' 重写数据库删除方法，实现逻辑删除 '''
        self.is_delete = True
        self.save()

```
