《千峰教育 django 视频教程》的学习笔记。

---

django 模板是用来快速生成页面的工具，支持简单的逻辑函数等。

模板的设计方式实现了 MVT 中的 VT 解耦，VT 具有 N:M 的关系，即一个视图函数可以调用任意模板，一个模板可供任意视图函数使用。

1.11 官方文档: [djangoproject docs](https://docs.djangoproject.com/en/1.11/)

## 1. 模板加载与渲染

模板处理分为 加载 和 渲染 两步。代码如：

```python
from django.template import loader
from django.shortcuts import render

# 加载
template = loader.get_template('app_index.html')
# 渲染
content = template.render()
# 返回
return HttpResponse(content)

# 实际中常用快捷函数
return render(request, 'app_index.html')
```

## 2. 模板基本语法

模板主要有两部分：html 静态代码 和 动态插入的代码段。模板中动态代码除了静态填充，还可以实现一些基本的运算、转换和逻辑（不应太复杂）。

### 2.1 注释

- 使用 `{# #}` 单行注释;
- 使用注释标签注释代码块：`{% comment %} foo {% endcomment %}`。

不可使用 html 的 `<!-- foo -->`，否则 html 页面中可以看到注释内容。

### 2.2 模板变量

模板中变量就是视图函数传递给模板的数据，也要遵循标识符命名规则。
语法为 {{ var }}，如果变量不存在，则模板渲染时插入空字符串。

### 2.3 模板点语法

模板中的点语法：

1. 字典查询；
2. 属性或者方法(方法传参较复杂) (eg: student.s_name)；
3. 索引 (eg: students.0.s_name)。支持查询集(queryset)。

如：
模型定义：

```python
class Student(models.Model):
    s_name = models.CharField(max_length=10)
    s_age = models.IntegerField(default=20)

    def get_info(self):
        return f'{self.s_name}: {self.s_age}. by method'
```

模板：

```jinja2
索引、字典：{{ studentsDic.0.s_name }}: {{ studentsDic.0.s_age }} <br>
属性：{{ student.s_name }} 方法：{{ student.get_info }} <br>
```

### 2.4 模板中标签

语法：大多数标签为成对，有开始有结束: `{% tag %} foo {% endtag %}`
    常见单个标签有: url 和 csrf_token，如`{% url 'namespace:name' p1 p2 %}`, `{% csrf_token %}`
作用：加载外部传入变量、输出中创建文本、控制循环或逻辑。

1. if 语句：

    ```jinja2
    {% if expr1 %}
        foo
    {% elif expr2 %}
        bar
    {% else %}
        baz
    {% endif %}
    ```

2. for 语句：

    ```jinja2
    {% for var in listORQueryset }
        foo
        {% empty %}  # 如果列表为空或不存在则执行 bar
            bar
    {% endfor %}
    ```

    for 语言循环体内支持循环次数查询，由以下变量记录

    - `forloop.counter`: 第几次循环，从 1 计数
    - `forloop.counter0`: 第几次循环，从 0 计数
    - `forloop.revcounter`: 第几次循环，倒着计数，1 为最后序号
    - `forloop.revcounter0`: 第几次循环，倒着计数，0 为最后序号
    - `forloop.first`: 是否为第一次循环
    - `forloop.last`: 是否为最后一次循环

3. 乘除: `{% widthradio num 分母 分子 %}`，即 此数乘以此分数。
    此处再提下整除，整除需要使用模板中过滤器: `{{ num|divisibleby:2 }}`

4. 比较
   - 大于等于小于运算符，只能在 if 标签中使用，如`{% if num > 5 %}`, `{% if num == 5 %}`
   - 判断是否相等的标签 `ifeuqual` 与 `ifnoteuqual`, 如`{% ifeuqual num1 num2 %} foo {% endifequal %}`

> 注意：在模板中除了过滤器要求不能空格之外各运算符或者标签之间最好有空格间隔。
> 例如上面的 > 需要空格间隔，而过滤器连接符 | 和参数均不能空格间隔，否则无法识别过滤器连接符或者参数不足。

示例：
使用 for 语句将列表展示为无序列表，并偶数行为橙色，且第 5 行为红色:

```jinja2
<ul>
    {% for student in studentsDic %}
        {% if forloop.counter == 5 %}
            <li style='color: red'>{{ student.s_name }}: {{ student.s_age }}</li>
        {% elif forloop.counter|divisibleby:2 %}
            <li style='color: orange'>{{ student.s_name }}: {{ student.s_age }}</li>
        {% else %}
            <li>{{ student.s_name }}: {{ student.s_age }}</li>
        {% endif %}

        {% comment %} {% ifequal forloop.counter 5 %}
            循环次数为 5
        {% endifequal %} {% endcomment %}
    {% endfor %}
</ul>
```

### 2.5 过滤器

作用：django 模板中不能对函数直接传参，所以处理一些数据时就要使用过滤器来操作。
语法：`{{ var|filter[:arg] }}`。可以使用在变量中，也可在标签中使用，如`{{ var|add:'2' }}`, `{% if var|divisibleby:2 %}`

常见过滤器，更多见官方文档: [djangoproject:Built-in template tags and filters](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#date)：

- `add:arg`: 当左右两边均是字符串时做字符串拼接，当左边是数值时做四则的加法(负数实现减法)，
    如: 字符串拼接`{{ studentsDic.0.s_name|add:'66' }}`, 加法`{{ studentsDic.0.s_age|add:66 }}`;
- `upper/lower`: 字符串转大小写，
    如: `{{ studentsDic.0.s_name|upper }}`;
- `default`: 如果变量会被 if 判断为 False，则就会使用提供的变量，
    如: `{{ ''|default:'aaa'}}`;
- `join:arg`: 将列表、字符串等等按照特定字符连接起来，
    如: `{{ studentsDic.0.s_name|join:'-' }}`;
- 'date:arg': 将 Python datetime 中实例转化成特定格式的字符串，注意格式中字母大小写含义不同见官方文档:[djangoproject:Built-in template tags and filters](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#date)，
    如: `{{ now_datetime|date:'y-m-d' }}`;
- `slice:arg`: 类似 Python 的切片，
    如: `{{ studentsDic|slice:'2:4' }}`;
- 'safe': 如果变量是 html 代码，则将其渲染，需要谨慎使用，要确保变量内容安全，
    如: `{{ code|safe }}`;

与 `safe` 相同用途的还有标签 `autoescape`，`off` 表示渲染 html，`on` 表示不渲染。如:

```jinja2
{% autoescape off %}
    {{ code }}
{% endautoescape %}
```

## 3. 模板的继承

模版继承：通过模板的结构标签让模板复用或者模板中某些部分( block )的重写。

结构标签：

- `block`:
    1. 块，用来在页面中“挖坑”，规划页面布局;
    2. 第一次出现代表规划（“挖坑”），第二次出现表示填充或者重写此规划的内容，如果不想重写则加 `{{ block.super }}` 保留原内容;
- `extends`: 继承，继承父模板中所有结构，必须是模板的第一个标签;
- `include`: 包含，可以将页面作为一个部分嵌入到模板中.

使用组合：

- `extends` + `block`: 父模板预先定义 block，子模板继承后将拥有父模板所有内容，并可以重写各个 block，若不想覆盖父模板内容，使用 `{{ block.super }}` 保留原内容。子模板中所有内容都必须在父模板定义的 block 中，否则不加载不渲染；
- `include` + `block`: 在各 block 中引入子页面;
- `extends` + `block` + `include`: 父页面可以使用引入子页面，子页面也可以在继承父模板的基础上再引入其他页面。

尽量少使用 `include`，效率低且容易引发难以察觉的异常，异常：在遇到语法或者模板不存的错误时，如果 settings 中`DEBUG = True`，则会正常引发 TemplateDoesNotExist 或 TemplateSyntaxError 错误，但如果`DEBUG = False`，则引入的子页面会为空字符串。

如：
`base.html`:

```jinja2
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{{ title }}</title>
    {% block ext_css %}
    {% endblock %}
</head>

<body>
    {% block header %}
        <h4>Base Header</h4>
    {% endblock header %}

    {% block content %}
        <h4>Base content</h4>
    {% endblock content %}

    {% block footer %}
        <h4>Base footer</h4>
    {% endblock footer %}
</body>

</html>
```

`child.html`:

```jinja2
{% extends "base.html" %}

{% block header %}
    {{ block.super }} {# 保留原内容 #}
    <h4>Child Header</h4>
{% endblock header %}

{% block footer %}
    {% include 'footer.html'%}
{% endblock footer %}

未在 block 中，不加载不渲染。

{% block notexist %}
    未在父 block 中，不加载不渲染。
{% endblock %}
```

`footer.html`:

```jinja2
<h4>include Footer</h4>
```

## 4. 模板静态文件

静态文件引入方式：

1. 在项目根目录下新建 *static* 文件夹，并在此文件夹下新建 js、css 的目录;
2. 在`setting` 中添加静态文件路径:

    ```python
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    ```

3. 模板中通过标签来加载和使用（仅限调试模式，否则需要单独处理，未学到后再补充）:

    ```jinja2
    {% load static %}

    {% static 'css/xxx.css' %}
    {% static 'js/xxx.js' %}
    ```

在模板继承时传参以后再学。
