Django 中视图用来接受 Web 请求，并作出响应。

视图本质就是一个 Python函数，其返回的响应有两种：

1. 以 json 数据形式返回
2. 以网页形式返回

视图响应的流程：浏览器发起请求 -> Django 获取信息并去掉 ip: 端口 -> urls 路由匹配 -> 视图响应 -> 返回给浏览器

## 1. url

Web 根路由配置具体目录设置在 `setting` 的 *ROOT_URLCONF*。实际中一般将项目划分成多个子应用，根路由的配置引入各个子应用的路由，根路由配置为：

```python
from django.conf.urls import url, include

urlpatterns = [
    url(r'^xxx/', include('App.urls')),
]
```

### 1.1 url 匹配规则

url 字符串加 `r` 使字符串不转义

url 正则匹配规则：正则匹配时按照 urlpatterns 中从上到下进行遍历，匹配到后停止向后查找；

例:
>一、对于下面的 url:
>
>```python
>urlpatterns = [
>    url(r'^hello', views.hello),
>    url(r'^hellooo', views.hellooo),
>]
>```
>
>访问以 *hello* 开头的任意地址均会匹配到 hello 视图函数，不会匹配到 hellooo 也不会 404。

url 书写规则:

1. 通常指定开头 `^`
2. 在除时间戳、随机串之外的 url，要加地址结束符。

**注意**: 地址结束符不能单一使用正则的 `$` 结束符，其会无法匹配带斜杠或不带斜杠的地址，如 `url(r'^end$', xxx)` 只有访问 end 才能匹配视图，访问 `end/` 无法匹配视图，会引发 404。要么使用 `/` 要么 `/$`，但是仅带 `/` 也有时也会有匹配问题，如下例。

例:
>仅带斜杠结束符
>
>```python
>urlpatterns = [
>    url(r'^geturlarg/', views.hello),
>    url(r'^geturlarg/(\d+)/', views.geturlarg)
>]
>```
>
>访问 *geturlarg/555* 仍然会错误地匹配到第一个，而进入 hello 视图，正确做法是再在斜杠后加正则结束符，即 修改第一个规则为 `r'^geturlarg/$'`

### 1.2 url 参数传递

使用正则匹配 `(pattern)` 以获取 url 中的参数。参数个数必须要一致，支持位置参数或关键字参数:

- 位置参数：按照书写顺序进行匹配；
- 关键字参数：按照参数名称匹配，与顺序无关，参数名必须一致，匹配规则的括号里加 `?P<argName>` 即可。

例:
>`urls.py`:
>
>```python
>urlpatterns = [
>    url(r'^geturlargs_p/(\d+)/(\d+)/', views.geturlargs_p),
>    url(r'^geturlargs_k/(?P<arg1>\d+)/(?P<arg2>\d+)/', views.geturlargs_k),
>]
>```
>
>`views.py`:
>
>```python
>def geturlargs_p(request, arg1, arg2):
>    info = f'position arg:\narg1: {arg1}, arg2: {arg2}, type: {type(arg1).__name__}'
>    return HttpResponse(info)
>
>
>def geturlargs_k(request, arg1, arg2):
>    info = f'key arg:\narg1: {arg1}, arg2: {arg2}, type: {type(arg1).__name__}'
>    return HttpResponse(info)
>```

### 1.3 反向解析

根据路径的标识动态获取路径。标识有子路由引入时 `include` 的 *namespace* 参数以及子路由路径的 *name* 属性；

获取路径：

- 在模板中使用标签获取：`{% url 'namespace:name' %}`
  - 位置参数：`{% url 'namespace:name' [arg1 arg2...] %}`
  - 关键字参数：`{% url 'namespace:name' [key1=v1 key2=v2...] %}`
- 在视图中使用: `redirect(reverse('namespace:name'))`, (redirect, reverse 在 `django.shortcuts` 里, shortcuts 里包含了常用的函数或者函数名缩写的函数)

如：
>视图函数其他同上，添加一个主页视图:
>
>```python
>def index(request):
>    return render(request, 'app_url.html')
>```
>
>根路由引入应用路由时填写 namespace 属性:
>
>```python
>from django.conf.urls import url, include
>
>urlpatterns = [
>        url(r'^appv/', include('app_url.urls', namespace='app_url')),
>]
>```
>
>在上面 `urls.py` 的基础上添加 name 属性:
>
>```python
>urlpatterns = [
>    url(r'^index/', views.index, name='index'),
>    url(r'^geturlargs_p/(\d+)/(\d+)/',
>        views.geturlargs_p, name='geturlargs_p'),
>    url(r'^geturlargs_k/(?P<arg1>\d+)/(?P<arg2>\d+)/',
>        views.geturlargs_k, name='geturlargs_k'),
>]
>```
>
>模板 *app_index.html* 反向解析获取 url
>
>```jinja2
>模板中使用 url 'namespace:name' [arg1 arg2...] 反向解析：
><a href="{% url 'app_url:index' %}">APP index</a><br>
>
>反向解析带url位置参数，参数为 555 444：
><a href="{% url 'app_url:geturlargs_p' 555 444 %}">geturlargs_position</a><br>
>
>反向解析带url关键字参数，参数为 arg1=111, arg2=222：
><a href="{% url 'app_url:geturlargs_k' arg1=111 arg2=222 %}">geturlargs_key</a><br>
>```

#### 错误页面定制

错误页面查找遵循最近原则，如果项目模板目录中没有就在 django 源码中寻找。故自定义错误页面在模板目录中创建对应错误代码的 html 文件即可。如 404 页面，新建 `404.html` 即可。

## 2. 请求与响应

### 2.1 请求(Request)

Django在接收到 Http 请求后，会根据报文创建 HttpRequest 对象。视图函数第一个参数就是 HttpRequest 对象。

HttpRequest 对象常用属性有:

- `path`: 请求的完整路径;
- `method`: 请求的方法，常用的 GET PUT 等;
- `encoding`: 编码方式，常用 utf-8;
- `GET`: 类似字典(QueryDict)，包含了 get 请求的所有参数;;
- `POST`: 类似字典(QueryDict)，包含了 post 请求的所有参数;
- `FILES`: 类似字典(QueryDict)，包含了上传的文件;
- `COOKIES`: 字典，包含了所有的 cookies;
- `session`: 类似字典(QueryDict)，表示会话;
- `META`: 包含服务器以及客户端的元信息，比如客户端的 ip: *REMOTE_ADDR* 等。

> 上面 QueryDict 的探查：
> 定义在 `django.http.request.QueryDict` 继承自 `django.utils.datastructures.MultiValueDict`，除具有字典的大部分特性外，加入了“多值”的特性。其将每个值都存为列表，`get(key)` 方法返回的是此值列表的最后一个元素，`getlist(key)` 才可返回全部元素。
>例子：
>
>```python
>from django.utils.datastructures import MultiValueDict
>
>multidic = MultiValueDict()
>multidic.setdefault('a', 1)
>multidic.setdefault('b', [11, 111])
>multidic.setlistdefault('lis', [2, 3])
>print(multidic)
># -> <MultiValueDict: {'a': [1], 'b': [[11, 111]], 'lis': [2, 3]}>
>print(multidic.get('a'))  # -> 1
>print(multidic.get('b'))  # -> [11, 111]
>print(multidic.get('lis'))  # -> 3
>print(multidic.getlist('lis'))  # -> [2, 3]
>```
>
>因为上面多值字典的特性，如果同一个请求中如果同一个参数传递多次，则此请求参数的值都会被保存下来。
>例子：如果请求参数为 *a=1&a=2&a=3*，则得到的数据为 `{'a': ['1', '2', '3']}`，对其使用 `get('a')` 只会拿到最后的 3，想获取全部需要使用 `getlist('a')`。

HttpRequest 对象常用方法: `is_ajax()`: 判断是否为 ajax()，常用于移动端和 JS 中。

### 2.2 响应(Response)

服务器返回给客户端的数据。

HttpResponse 创建有两种途径:

- 不使用模板：直接返回 `HttpResponse()`;
- 使用模板：可以使用 `render` 创建或者自己先加载模板再渲染。

HttpResponse 常用属性:

- `content`: 返回的内容;
- `charset`: 编码格式;
- `status_code`: 响应状态码;
- `content_type`: MIME 类型

> MIME(Multipurpose Internet Mail Extensions):
>设定某种扩展名的文件用一种应用程序来打开的方式类型,
>格式：大类型/小类型，如: image/png, image/jpeg

常用方法:

- `init`: 初始化内容;
- `write(xxx)`: 直接写文本;
- `flush`: 冲刷缓冲区。但实际上源码里此函数未实现任何功能;
- `set_cookie(key, value='', max_age=None, expires=None)`: 设置 cookie
- `delete_cookie(key)`: 删除 cookie

HttpResponse 常用子类:

- `HttpResponseRedirect/HttpResponsePermanentRedirect`: 响应临时/永久重定向，实现服务器内部跳转，其快捷: `django.shortcuts.redirect`。条件性或临时性重定向使用前者，只有永久性重定向才使用后者;
  - 直接写 url: `redirect('/app/index')`;
  - 更推荐使用反向解析: `redirect(reverse('namespace:name'))`
- `JsonResponse`: 返回 json 数据额请求，通常用于异步请求上。
- 其他子类均在源码 `django.http.response` 中，大多都只是更改了响应状态码。

## 3. 会话技术

会话技术是为了解决在 Web 开发中基本都是短连接的 http 下（生命周期为从请求开始到响应结束），服务器识别客户端的问题。

会话技术有三种: Cookie, Session, Token.

- Cookie: 客户端会话技术，数据存储在客户端。
  - 特性：数据以键值对存储，支持过期时间，默认 Cookie 会自动携带，Cookie不能跨域名或网站;
  - 生成 Cookies: 服务器通过 HttpResponse 来生成 cookie;
  - 弊端: cookie 依赖浏览器(其他客户端可能不支持 cookie)。
- Seession: 服务端会话技术，数据储存在服务器。
  - 默认 session 存储在内存中，考虑分布式服务器，需要将 session 持久化。Django 中默认将 session 持久化到数据库中(数据表 django_session);
  - 依赖 cookie，session 的唯一标识需要存到 cookie 中，服务端借此区分客户端;
  - 弊端: session 依赖 cookie 故存在于 cookie 相同弊端。
- Token: 服务端会话技术，可以理解为自定义的 session，是有自己生成的唯一串。
  - 不依赖于 cookie;
  - 在 Web 页面中，使用起来与 session 相同;
  - 在移动端或其他客户端中，通常以 json 形式传输，需要移动端存储 token，需要获取 token 关联数据时需要主动传递 token。
- 三者对比:
  - cookie 使用简单，服务器压力小，数据不是很安全;
  - session 服务器要维护 session，相对安全;
  - token 拥有 session 优点，且支持更多终端，但维护麻烦。

### 3.1 Cookie

`response.set_cookie(key, value, max_age=None, expires=None)`:

- max_age: 指定 cookie 过期时间，以秒为单位的整数;
- expires: `datetime.datetime` 对象或者时间格式的字符串（时间字符串格式很繁琐，不推荐使用）（测试发现，expires 过期后浏览器不会清除 cookie，很奇怪）。

几个特殊的时间设定:

1. max_age 为 0 表示浏览器关闭失效;
2. max_age 为 None 时为永不过期;

另外通过看源码发现：如果其是 `datetime.datetime` 对象，最终都会计算为 max_age 并清空；如果 max_age 和 `datetime.datetime` 的 expires 都设置了，最终会以 expires 为准。例:

```python
response.set_cookie(
    'username', username,
    max_age=60,
    expires=datetime.now() + timedelta(days=1),
)
# 这段代码设置的 cookie 过期时间是一天后，而不是 60 秒后。
```

cookie 获取: `request.COOKIES.get('username')`

cookie 默认不支持中文，部分 Web 框架会通过中英文转化实现中文的支持，比如 base64 编码，也可以使用 `json.dumps/loads` 进行相互转化(dumps/loads 可以将中文编码/解码成 Unicode)。

cookie 加密: `response.set_signed_cookie(key, value, salt='', **kwargs)`;
解密: `request.get_signed_cookie(key, salt='', **kwargs)`。加密解密的 salt 要一致。

>例子，
>（登陆页面与登陆逻辑未内聚到一个视图函数）:
>
>```python
>def login(request):
>    return render(request, 'app_cookie_login.html')
>
>
>def do_login(request: HttpRequest):
>    # 实际上，一般将这部分也写到 login 视图中，通过 request.method 来>区分请求。这样登陆就具有了内聚特点
>    username = request.POST.get('username')
>
>    response = redirect(reverse('app_cookie:logged'))
>    response.set_cookie(
>        'username', username,
>        max_age=20,
>        # expires=datetime.now() + timedelta(seconds=20),
>    )
>    # response.set_signed_cookie(
>    #     'username', username,
>    #     salt='salt',
>    #     # max_age=50,
>    # )
>    return response
>
>
>def logged(request: HttpRequest):
>    try:
>        username = request.COOKIES.get('username')
>        # username = request.get_signed_cookie('username', >salt='salt')
>
>        if username:
>            return render(request, 'app_cookie_logged.html',
>                          context={'username': username})
>    except Exception:
>        pass
>    return redirect(reverse('app_cookie:login'))
>
>
>def logout(request):
>    response = redirect(reverse('app_cookie:login'))
>    response.delete_cookie('username')
>
>    return response
>```

### 3.2 Session

Django 中默认将 session 持久化到数据表 *django_session*，故使用 session 一般需要先 `migrate` 迁移。django 内置的 session 通过 settings 的 *INSTALLED_APPS* 和 *MIDDLEWARE* 引入，不使用可以注释。

session 是 HttpRequest 的属性，类似字典(QueryDict)对象，上面 #2.1 有说明，其支持中文。

session 常用操作:

- `session[key] = value`: 设置 session。创建 session 数据并保存到数据表中，数据表有三个字段:

  - session_key: 主键，最大长度为 40，此值也会保存在 cookie 的 *sessionid* 字段;
  - session_data: 混淆串加原始 key-value 的 base64 编码字符串，如果是中文其会先将中文转 Unicode;
  - expire_date: 过期时间。

- `session.set_expiry(value)`: 设置 session 过期时间，可以为整数和 datetime 类型以及 None:
  - value 为整数: 秒为单位的过期时间，0 时表示浏览器退出就过期;
  - value 为 datetime 或 timedelta，过期日期;
  - value 为 None 时采用 `settings` 的过期时间;
  - 注意: 过期后数据库中仍然存在过期的数据，使用 `python manage.py clearsessions` 来清除（推荐定时操作）。
- `session.get(key, default=None)`: 根据键获取上面设置的原始 value;
- `session.clear()`: 清除所有会话？？？;
- `session.flush()`: 删除当前会话数据(数据库)以及 cookie;
- `session.session_key`: 获取当前 session 的 session_key;

> 注意: session 删除使用 `session.flush()` 即可，不能使用下面的方法:
>
> - 单纯删除 `session[key]`，如 `del request.session['username']`，其会从数据表的 `session_data` 字段中清除原 key-value 的信息，但此条数据仍然在数据库中，且客户端仍然存在 cookie;
> - 单纯删除 sessionid 的 cookie，如 `resp.delete_cookie('sessionid')` 无法删除服务端的 session，数据表中仍存在那条数据

>例子:
>
>```python
>def login(request: HttpRequest):
>    if request.method == 'GET':
>        return render(request, 'app_session_login.html')
>    elif request.method == 'POST':
>        username = request.POST.get('username')
>
>        request.session['username'] = username
>        request.session.set_expiry(600)
>
>        return redirect(reverse('app_session:logged'))
>
>
>def logged(request: HttpRequest):
>    username = request.session.get('username')
>
>    if username:
>        return render(request, 'app_session_logged.html',
>                      context={'username': username})
>    # except Exception as e:
>    #     pass
>    return redirect(reverse('app_session:login'))
>
>
>def logout(request: HttpRequest):
>    print(request.session.session_key)
>
>    response = redirect(reverse('app_session:login'))
>
>    # wrong
>    # response.delete_cookie('sessionid')
>    # del request.session['username']
>
>    # correct
>    request.session.flush()
>    # request.session.clear()  # 清除所有???
>
>    return response
>```

### 3.3 Token

基于 Token 的验证流程:

1. 客户端登陆;
2. 服务端收到请求后验证用户信息;
3. 验证成功后，服务端生成 Token，并发给 客户端;
4. 客户端收到后将 Token 保存起来，如存到 Cookie;
5. 客户端每次发送请求时带上 Token;
6. 服务端收到请求后验证 Token，验证成功则向客户端返回请求的数据。

对于 Token 生成方法，可以使用 `hashlib.new('algorithm', data=b'').hexdigest()` 来生成，其中 data 要求为字节型，可以使用 `str.encode()` 转化为字节型。

>例子:
>
>```python
>def register(request: HttpRequest):
>    if request.method == 'GET':
>        return render(request, 'app_token_reg.html')
>    elif request.method == 'POST':
>        username = request.POST.get('username')
>        password = request.POST.get('password')
>
>        try:
>            student = Student()
>
>            student.s_name = username
>            student.s_password = password
>
>            student.save()
>        except Exception:
>            return redirect(reverse('app_token:register'))
>
>        return HttpResponse('注册成功')
>
>
>def generate_token(ip, username):
>    '''generate unique token'''
>    c_time = ctime()
>    r = username
>
>    token = hashlib.new('md5', (ip + c_time + r).encode('utf-8')).>hexdigest()
>
>    return token
>
>
>def login(request: HttpRequest):
>    if request.method == "GET":
>        return render(request, 'app_token_login.html')
>    elif request.method == 'POST':
>        username = request.POST.get('username')
>        password = request.POST.get('password')
>
>        students = Student.objects.filter(
>            Q(s_name=username) & Q(s_password=password))
>
>        if students.exists():
>            student = students.first()
>
>            ip = request.META.get('REMOTE_ADDR')
>            token = generate_token(ip, username)
>            student.s_token = token
>            student.save()
>
>            # response = HttpResponse('登陆成功')
>            # response.set_cookie('token', token)
>            # return response
>            data = {
>                "status": 200,
>                "msg": "login success",
>                "token": token
>            }
>            return JsonResponse(data=data)
>        # return redirect(reverse('app_token:login'))
>        data = {
>            "status": 800,
>            "msg": "verify failed",
>        }
>        return JsonResponse(data=data)
>
>
>def logged(request: HttpRequest):
>    # token = request.COOKIES.get('token')
>    token = request.GET.get('token')
>    try:
>        student = Student.objects.get(s_token=token)
>    except Student.DoesNotExist:
>        return redirect(reverse('app_token:login'))
>    # return HttpResponse(student.s_name)
>    data = {
>        "status": 200,
>        "msg": "ok",
>        "data": {
>            'username': student.s_name
>        }
>    }
>    return JsonResponse(data=data)
>```

### 3.4 csrf

在表单提交时加验证，防止跨站攻击，确保客户端是本服务端的客户，在表单内加标签 `{% csrf_token %}`。

django 通过 `settings` 的 *MIDDLEWARE* 引入 `csrf.CsrfViewMiddleware`中间件来实现，其在存在 `{% csrf_token %}` 的页面中，表单内自动生成隐藏的 input 标签，标签 name 为 csrfmiddlewaretoken, value 包含一串字符串。客户端访问时服务端的响应会给客户端设置一个key为 csrftoken 的 cookie。服务端收到表单提交请求后会先验证 csrfmiddlewaretoken 和 csrftoken。

>例子：
>
>```html
><form action="{% url 'app_token:login' %}" method="post">
>    {% csrf_token %}
>    <span>用户名</span><input type="text" name="username" >placeholder="请输入用户名">
>    <br>
>    <span>密码</span><input type="text" name='password' >placeholder="请输入密码">
>    <br>
>    <button>登陆</button>
></form>
>```

## 4. 其他

- 编码解码
  - base64
  - urlencode
- 摘要算法、指纹算法
  - 常用算法: md5, sha
    - md5 默认 128位，即 32长度的十六进制，python 为字符串类型(unicode编码)
  - 单向不可逆
  - 根据内容数据生成的一串字符串，不管输入长度，输出总是固定长度
  - 输入微小变化，输出都会发生巨大变化
- 加密算法
  - 对称加密: 解密和加密的密钥相同，如 DES, AES。优点: 加密解密效率高，但密钥泄露后果严重
  - 非对称加密: 解密和加密的密钥不相同，公钥一般 1024 位，私钥 2048 位。如 RSA, PGP。优点是安全性最高，但需要时间和空间资源较大

## 5. 问题遗留

MTV 基本完成，但遗留 Model 的关系(一对多等等) 以及 Model 继承。

高级:

- 第三方插件;
- 底层部分原理:
  - AOP 面向切面编程:
    - 反爬;
    - 安全
- 文件上传;
- 前后端分离;
  - RESTful
- 日志
- 后台管理
- 用户角色、用户权限
- 项目部署
- 支付宝支付、微信支付
