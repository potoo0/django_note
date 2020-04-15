《千峰教育 django 视频教程》的学习笔记。

---

## 1. django 设计模式

django 采用 MVC 框架模式，有时也称 MVT 模式。

MVC 模式简介：

- Model: 封装业务逻辑相关的数据，web 中用来处理数据逻辑部分。Model 通常只提供功能性接口；
- View: 负责数据的显示和呈现，是对用户的直接输出；
- Controller: 负责从用户端收集用户输入，可看做 View 的反向功能，主要处理用户交互。

MVT 简介：

- Model: 负责业务对象与数据库 (ORM) 的对象；
- View: 负责业务逻辑，并在适当的时候调用 Model 与 Template；
- Template: 负责把页面呈现给用户。

> django 还有个 url 分发器（路由），用于将不同的 url 分发给不同的 View。


## 2. django 项目结构

通过 `django-admin startproject projectName .` 创建项目到当前文件夹。创建后下有下面这些文件：

- `manage.py`: 管理项目，如用于创建 app 以及项目启动等。
- `projectName`(以下称 web 根目录):
  - `__init__.py`: 文件夹作 python module，早期版本会在此处加入使用 pymysql 伪装 MySQLdb;
  - `settings.py`: 项目配置，包括路径、数据库、模板等；
  - `urls.py`: 项目根路由；
  - `wsgi.py`:  项目部署时使用。

> 此处再说明下 项目名后的参数 `.` ：指定创建项目到当前文件夹，而不创建外层文件夹。
>
> 这么做的原因是我自己的操作流程习惯：文件管理器创建项目文件夹 -> 使用 vscode 打开此文件夹 -> vscode 中创建项目到当前文件夹。）

### 2.1 `settings.py`

常用设置：

- *DEBUG*: 是否打开调试，如果此值为 False 表示不打开调试，则此时必须配置 *ALLOWED_HOSTS*；
- *ALLOWED_HOSTS*: 添加 `‘*’` 以允许所有 ip 访问；
- *INSTALLED_APPS*: 此处需要添加创建的 app 目录名到此处；
- *MIDDLEWARE*: 中间件；
- *ROOT_URLCONF*: 根路由；
- *TEMPLATES*: 模板目录，后期需要修改到与 `manage.py` 并列，因为可能多个 app 的模板之间需要继承；
- *WSGI_APPLICATION*: 项目部署使用；
- *DATABASES*: 修改数据库，以及连接的参数；
- *TIME_ZONE*: 时区，中国时区为 `Asia/Shanghai`；
- *STATIC_URL*: 静态文件。

此处先大致说下项目配置后 `settings.py` 一般需要修改的：

1. 把创建的 app 添加到 *INSTALLED_APPS*；
2. 项目根目录下(`manage.py` 同级)创建 templates 文件夹，并在 *TEMPLATES* 的 *DIRS* 添加此文件夹路径，如:

    ```python
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    ```

3. 如果使用了数据库，需要在 *DATABASES* 下添加数据库配置，如：

    ```python
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'django01',
    'USER': 'root',
    'PASSWORD': 'testpass',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},  # 数据库编码
    # create table: CREATE DATABASE `django01` CHARACTER SET 'utf8mb4';
    ```

    如果使用的是 mysql，早期 django 版本还需要在 `__init__.py` 中添加：

    ```python
    import pymysql
    
    pymysql.install_as_MySQLdb()
    ```

4. 修改时区为：`Asia/Shanghai`
5. 静态文件（以后补充）。

### 2.2 `urls.py`

web 根目录下的路由通常不直接关联某个应用视图，由 `include` 来引入 app 的路由，如：

```python
from django.conf.urls import url, include

urlpatterns = [
    url(r'^app/', include('App.urls', namespace='app')),
]
```

### 2.3 app

django 设计 web 时通常根据解耦的思想划分子应用，每个应用都是一个包（与项目根目录同级）。项目下创建如下：

```powershell
python manage.py startapp appName
```

创建的 app 结构如下：

- `__init__.py`: 同上，作为包；
- `admin.py`: 后台管理相关的设计；
- `apps.py`: app 的配置，如重写 app 的 name；
- `models.py`: MVT 设计模式的 *Model*，负责业务对象与数据库 (ORM) 的对象，提供接口供 `views.py` 部分调用；
- `tests.py`: 测试代码；
- `urls.py`: (需手动创建) url 分发器(路由)，将 url 分发给对应的视图函数(view)；
- `views.py`: MVT 设计模式的 *View*，负责业务逻辑，包括多个视图函数，并在适当的时候调用 `models.py` 提供的接口与 Template；
- `migrations`: 一个包含数据库对接所需中间文件的文件夹，由 `manager.py` 生成和执行。

> 注意：如果使用的虚拟环境，那 vscode 还需要激活此虚拟环境，详细见上文，此处再重述：
    ```powershell
    $mypwd=pwd; cd E:\django_note\python36_django\Scripts; .\activate; cd $mypwd # 路径修改为自己的
    ```

## 3. `manage.py` 常用命令总结

- `startapp appName`: 创建名称为 appName 的应用；
- `shell`: 此项目的命令行，可用于调试等等；
- `makemigrations`: 基于模型的修改创建迁移；
- `migrate`: 应用和撤销迁移；
- `runserver [[ip:]port]`: 启动项目，vscode 通常通过 debug 启动，IP和端口号追加到 `launch.json` 的 *args*。

---

## 4. 示例工程

1. 进入 python 虚拟环境:

    ```powershell
    $mypwd=pwd; cd E:\django_note\python36_django\Scripts; .\activate; cd $mypwd
    ```

2. 创建工程:

    ```powershell
    django-admin startproject Hello .
    ```

3. 新建 app:

    ```powershell
    python manage.py startapp helloworld
    ```

4. 新建通用模板目录:

    ```powershell
    mkdir templates
    ```

5. 修改 `Hello` 文件夹下 `settings.py` 中对应设置:
    1. 修改 *ALLOWED_HOSTS*: `ALLOWED_HOSTS = ['*']`
    2. *INSTALLED_APPS* 添加: `'helloworld'`
    3. *TEMPLATES* 修改 *DIRS*: `'DIRS': [os.path.join(BASE_DIR, 'templates')],`
    4. 修改自己数据库信息。
    5. 修改时区 *TIME_ZONE*: `TIME_ZONE = 'Asia/Shanghai'`
    6. 关闭时区表 *USE_TZ* 防止 MySQL datatime 时区不统一: `USE_TZ=False`
6. 操作数据库还需要迁移:

    ```powershell
    python .\manage.py makemigrations  # 生成模型的迁移文件
    python .\manage.py migrate  # 应用和撤销迁移
    ```
