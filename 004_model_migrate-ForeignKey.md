Django 模型的迁移与一对多等对应关系。

## 1. 模型迁移原理

Django 模型迁移分两步:

1. 生成迁移文件，`makemigrations` 命令;
2. 执行迁移文件，`migrate` 命令

迁移文件的生成:

- 根据 models 或者文件生成对应的迁移文件;
- 根据 models 和已有的迁移文件差异，生成新的迁移文件。迁移文件也是增量式，每个新迁移文件都是根据模型文件的新变化生成。

执行迁移过程:

- 先去迁移记录查找未迁移的文件，根据 app 名和迁移文件的名字判断;
- 执行未迁移的文件;
- 执行完成后，记录新执行的迁移记录

其中迁移文件名命令是app 的第一个迁移文件命令为序号+initial，其后的迁移文件是增序序号+模型名的命令方式。迁移记录在 *django_migrations* 数据表，主要信息包含 app 名和迁移文件名。

重新迁移:

- 删除迁移文件;
- 删除迁移生成的数据表;
- 删除迁移记录( 位于数据表 *django_migrations*)。

## 2. 模型级联关系

数据库主键、外键、主表、从表概要:

- 主键(primary key): 数据表中一个或者多个字段，数据类型不限，其值用于唯一标识表的一条记录;
  - 联合主键: 通过多个字段唯一标识记录。
- 外键(foreign key): 让多个表产生组织关系。通过定义外键约束实现，其值是主表的主键值或null;
- 主表: 被作为外键引用的表；
- 从表: 有外键约束的表，即声明关系的表。

数据表的级联通过外键实现，数据表级联按照对应关系可分为:

- 一对一：外键放那张表都可以；
- 一对多：外键放多的那张表，外键加唯一约束，如 班级-学生 例中，如果学生数量大于班级数量，那外键应放学生表；
- 多对多：外键放新建的中间表，外键加联合唯一约束。

级联关系越复杂，则效率越低，实际中尽量避免。

### 2.1 一对一关系

两种应用场景:

1. 复杂表拆分。某表字段太多，且字段数据长度较长，此时需要将表拆分成多表;
2. 数据表的扩展，在当前表上扩展字段采用此方法，可以避免删除原表。如，要在一张已有的用户表上增加 token 字段。

创建: Django 中使用 `models.OneToOneField(tableName)` 在表中声明一对一字段，通常此字段允许为空以及空字符串( `null=True, blank=True,` )。一对一字段在数据表中实现为：对外键添加唯一约束，如:

```sql
UNIQUE KEY `id_person_id` ( `id_person_id` ),
CONSTRAINT `app_oneToOne_idcard_id_person_id_56ff10d3_fk_app_oneTo` FOREIGN KEY ( `id_person_id` ) REFERENCES `app_onetoone_person` ( `id` )
```

关系绑定：将主表单个记录赋值到从表对应显性属性;

删除: Django 中默认级联表的删除动作(字段的 `on_delete` 属性)为 `CASCADE`：从表删除、主表不受影响；主表删除，从表对应数据也删除;

删除动作总结:

- `models.CASCADE`: 从表删除、主表不受影响；主表删除，从表对应数据也删除;
- `models.PROTECT`: 主表存在级联数据时，主表此记录受保护，可先删除从表的级联数据再删除主表此记录。开发中防止误操作常使用此模式。
- `models.SET`: 删除主表时，对从表中对应字段设置值，有以下三种:
  - `models.SET_NULL`: 空值，需要设置此字段允许为空;
  - `models.SET_DEFAULT`: 一对一关系中，不能使用，会与唯一约束发生冲突;
  - `models.SET(value)`: 一对一关系中，不能使用，会与唯一约束发生冲突;

查询:

- 从表查主表: 显性属性，即属性名。返回为一条主表记录;
- 主表查从表: 隐性属性，为级联模型名称（一般为小写），返回为一条从表记录，。

>例子:
>一对一模型声明:
>
>```python
>class Person(models.Model):
>    p_name = models.CharField(max_length=16)
>    p_sex = models.BooleanField(default=False)
>
>
>class IDcard(models.Model):
>    id_num = models.CharField(max_length=18, unique=True)
>    id_person = models.OneToOneField(
>        Person,
>        null=True, blank=True,
>        on_delete=models.SET_NULL)
>```
>
>测试（推荐在 django shell 下测试）:
>
>```python
>from app_oneToOne.models import Person, IDcard
>
># 添加 person
>person = Person.objects.create(p_name='Rick')
># 添加 idcard，先不与主表记录绑定
>idcard = IDcard.objects.create(id_num=46465)
># 绑定从表与主表记录
>person = Person.objects.last()
>idcard = IDcard.objects.last()
>idcard.id_person = person
>idcard.save()
>
># 删除最新的 person
>person = Person.objects.last()
>person.delete()
># 删除最新的 idcard
>idcard = IDcard.objects.last()
>idcard.delete()
>
># 从查主:
>idcard = IDcard.objects.last()
>person = idcard.id_person  # 一条 Person 记录
>person.p_name
># 主查从:
>person = Person.objects.last()
>idcard = person.idcard  # 一条 Idcard 记录
>idcard.id_num
>```
>

### 2.2 一对多关系

创建: Django 中使用 `models.ForeignKey(tableName)` 在表中声明一对多字段;
关系绑定：将主表单个记录赋值到从表对应显性属性;
删除：同一对一;
查询:

- 从查主: 显性属性，即属性名。返回为一条主表记录;
- 主查从: 隐性属性为级联模型_set，Manager 的子类，返回同 Manager 的返回( QuerySet )，支持 `all`, `values`, `get`, `fliter`等等;

>例子:
>一对多模型声明:
>
>```python
>class Grade(models.Model):
>    g_name = models.CharField(max_length=10)
>
>
>class Student(models.Model):
>    s_name = models.CharField(max_length=10)
>    s_age = models.IntegerField(default=20)
>    s_grade = models.ForeignKey(
>        Grade,
>        null=True, blank=True,
>        on_delete=models.CASCADE)
>```
>
>测试（推荐在 django shell 下测试）:
>
>```python
>from app_oneToMany.models import Grade, Student
>
># 添加 grade
>grade = Grade.objects.create(g_name='class_04')
># 添加 student，包括 s_grade
>student_1 = Student()
>student_1.s_name = 'Rick_1'
>student_1.s_grade = Grade.objects.last()
>student_1.save()
>student_2 = Student()
>student_2.s_name = 'Rick_2'
>student_2.s_grade = Grade.objects.last()
>student_2.save()
>
># 删除最新的 grade
>grade = Grade.objects.last()
>grade.delete()
># 删除最新的 idcard
>student = Student.objects.last()
>student.delete()
>
># 从查主:
>student = Student.objects.last()
>grade = student.s_grade  # 一条 grade 记录
>grade.g_name
># 主查从:
>grade = Grade.objects.last()
>students = grade.student_set  # QuerySet 集合，包含所有满足的 student
>students.values()  # 字典输出
>```
>

### 2.3 多对多关系

较复杂，实际中很少直接使用多对多属性，而通常自己构造和维护。

多对多实现为：对主表和从表中不涉及级联数据，而是新建一张“从表名_多对多字段名”的关系表，此关系表使用外键的联合约束，即外键值不能同时相同，如:

```sql
CREATE TABLE `app_manytomany_goods_g_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `goods_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_manyToMany_goods_g_c_goods_id_customer_id_2b8f1dc6_uniq` (`goods_id`,`customer_id`),
  KEY `app_manyToMany_goods_customer_id_f9e494f2_fk_app_manyT` (`customer_id`),
  CONSTRAINT `app_manyToMany_goods_customer_id_f9e494f2_fk_app_manyT` FOREIGN KEY (`customer_id`) REFERENCES `app_manytomany_customer` (`id`),
  CONSTRAINT `app_manyToMany_goods_goods_id_6e2af680_fk_app_manyT` FOREIGN KEY (`goods_id`) REFERENCES `app_manytomany_goods` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

创建: Django 中使用 `models.ManyToManyField(tableName)` 在表中声明一对多字段;
关系操作（即操作关系表）:

- 从操作主: 通过显性属性（从表对应字段名），其是 `ManyRelatedManager`子类;
- 主操作主: 通过隐性属性（从表名_set），其也是 `ManyRelatedManager`子类，同从操作主具有完全相同的方法;

`ManyRelatedManager` 基本内容:

- `ManyRelatedManager` 是 `django.db.models.fields.related_descriptors` 中函数`create_forward_many_to_many_manager` 动态创建，父类有函数参数动态指定，其继承了 `models.Manager`;
- `ManyRelatedManager` 返回 `QuerySet`，查询操作同objects 管理器，如 `all`, `values`, `get`, `fliter`等等;
- 支持的增删操作有（不需要再执行 `save`）:
  - `add`: 添加，传入单组主表或者从表记录;
  - `remove`: 删除，传入单组主表或者从表记录;
  - `clear`: 清除，如 `custom.goods_set.clear()` 将清除关于记录 custom 的级联数据;
  - `set`: 批量添加，如 `custom.goods_set.set(goods_queryset)` 将 custom 与每个 goods_queryset 添加关系;
- 上面级联数据的操作均做了兼容性处理，添加重复的记录或者删除不存在均不会抛出异常。

删除：如上面属性的 `remove` 和 `clear`;

>例子:
>多对多模型声明:
>
>```python
>class Customer(models.Model):
>c_name = models.CharField(max_length=50)
>
>
>class Goods(models.Model):
>g_name = models.CharField(max_length=50)
>g_customer = models.ManyToManyField(Customer)
>```
>
>测试（推荐在 django shell 下测试）:
>
>```python
>from app_manyToMany.models import Customer, Goods
>
># 添加 customer
>for index in range(4):
>customer = Customer.objects.create(c_name=f'Rick_{index:03}')
># 添加 goods，并绑定关系
>for index in range(3):
>goods = Goods.objects.create(g_name=f'item_{index:03}')
>
># add: 绑定单个
>customer = Customer.objects.all()
>goods = Goods.objects.all()
>for c in customer:
>for g in goods:
>   c.goods_set.add(g)
># remove: 删除单个
>c.goods_set.remove(g)
># clear: 删除全部满足的
>c.goods_set.clear()
># set: 绑定多个
>c.goods_set.set(goods)
>
># 主从其他操作也均相同，如查询:
>g_last = goods.last()
>print(g_last.g_customer.filter(pk__gt=2).values())
>```

## 3. 模型继承

模型继承：使子模型拥有父模型的字段，且父模型不在数据库生成映射。需要将父模型抽象化，实现为在父模型定义 `Meta` 中加入字段: `abstract = True`。

>例子:
>模型定义:
>
>```python
>class Animal(models.Model):
>    a_age = models.IntegerField(default=2)
>
>    class Meta:
>        abstract = True
>
>
>class Cat(Animal):
>    c_name = models.CharField(max_length=50)
>
>
>class Dog(Animal):
>    d_name = models.CharField(max_length=50)
>```

如果不加，那父模型也会在数据库中生成，子模型中主键为外键，即形成了一对一关系。

## 4. Sql2Model

上面均是 Model2Sql，即使用 django 创建 model 并通过迁移与数据表产生映射。但在实际中数据表可能不是由自己设计，则需要根据已有数据表生成 model，建立模型与数据表的映射。

命令为:

```bash
# python manage.py help inspectdb  # 查看帮助
# python manage.py inspectdb  # 当前连接的数据库下所有数据表
# python manage.py inspectdb table  # 当前连接的数据库下特定数据表
# 例子
python manage.py inspectdb app_modelinheritance_cat >> app/models.py
```

生成的模型元信息中包含 `managed = False`，其作用为：django 不更改此数据表，如新建、字段修改、删除。

## 5. 静态资源与文件上传

### 5.1 静态资源

静态资源中 html 不会经过模板渲染，实际中效率较高。

在 <002_templates.md##4. 静态文件> 中有总结用法，此处内容再复制一次。

静态文件引入：

1. 在项目根目录下新建 *static* 文件夹，并在此文件夹下新建 js、css 的目录;

2. 在`setting` 中添加静态文件路径:

    ```python
    STATIC_URL = '/static/'  # static 文件的 url

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    ```

3. 静态文件可以直接访问，如 `localhost/static/html/static_html.html`。

4. 模板中通过标签来加载，无须写 URL（仅限调试模式，否则需要单独处理，未学到后再补充）:

    ```jinja2
    {% load static %}

    {% static 'css/xxx.css' %}
    {% static 'js/xxx.js' %}
    ```

### 5.2 文件上传

#### 5.2.1 上传页面

表单上传文件需要以 post 方式，且需要属性 `enctype='multipart/form-data'` 不对字符编码。

>例子:
>
>```html
><form action="{% url 'app_uploadFiles:upload' %}" method="POST" enctype="multipart/form-data">
>    {% csrf_token %}
>    <span>文件:</span><input type="file" name="icon">
>    <br>
>    <input type="submit" value="上传">
></form>
>```

#### 5.2.2 文件存储

上传的数据存储在 `request.FILES` 中。

##### a. 手动储存

读取 `request.FILES`, 以二进制写入到文件。

>例子:
>
>```python
>def upload(request: HttpRequest):
>    if request.method == 'GET':
>        return render(request, 'app_upload.html')
>    elif request.method == 'POST':
>        icon = request.FILES.get('icon')
>        with open(r'static\uploadFiles\icon.jpg', 'wb') as fp:
>            for chunk in icon.chunks():
>                fp.write(chunk)
>                fp.flush()
>        return HttpResponse('upload success')
>```

##### b. 模型字段储存

django 的模型中包装了对文件操作的字段，可以快速简洁地完成文件上传。以 ImageField 为例，其比 FileField 多 width_field 和 height_field 两个属性，其余均相同。

字段中 upload_to 为文件存储的相对路径，其路径是相对于媒体根目录，路径中支持时间字符串，用以将上传的文件按照时间分割到不同文件夹（实际中建议添加，因为操作系统中文件夹的文件数量存在上限）。媒体根目录由 `settings` 的 `MEDIA_ROOT` 确定，URL 由 `MEDIA_URL` 确定。

如果文件名和路径完全一样，django 在存储时会为文件加随机字符串以保证其唯一性。

此字段不会将文件的二进制存储至数据库，在数据库中是文件路径的字符串。

其常用的属性有 `url`，可以返回访问文件的 URL。

>例子:
>`settings.py`:
>
>```python
>MEDIA_URL = '/media/'
>MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
>```
>
>`models.py` 定义 ImageField 字段:
>
>```python
>class UserModel(models.Model):
>    u_name = models.CharField(max_length=50)
>    u_icon = models.ImageField(upload_to='icons/%Y-%m')
>```
>
>`urls.py`:
>
>```python
>url(r'^imagefield/', views.image_field, name='image_field'),
>url(r'^geticon/', views.get_icon, name='get_icon'),
>```
>
>`views.py`:
>
>```python
>def image_field(request: HttpRequest):
>    if request.method == 'GET':
>        return render(request, 'image_field.html')
>    elif request.method == 'POST':
>        uname = request.POST.get('uname')
>        icon = request.FILES.get('icon')
>
>        user = UserModel()
>        user.u_name = uname
>        user.u_icon = icon
>        user.save()
>
>        return HttpResponse(f'user: {user.id} upload success')
>
>
>def get_icon(request: HttpRequest):
>    uname = request.GET.get('uname')
>
>    user = UserModel.objects.get(u_name=uname)
>    # print(f'dir: {dir(user.u_icon)}')
>    print(f'.url: {user.u_icon.url}')  # 图片 url
>
>    return HttpResponse(f'.url: {user.u_icon.url}')
>```

如果需要通过文件 URL 直接访问文件，还需要在路由中调用 `server()` 视图，具体见下例子。（官方不推荐在生成环境中使用）

例:

```python
from django.views.static import serve
from model_migrate_ForeignKey.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
```
