## 1. 缓存

缓存同来提升服务器响应速度。方法是将执行过的数据存储下来，再次获取数据时，直接从缓存中获取。理想方案是将数据缓存到内存中。

缓存框架的核心目标:

- 较少的代码。缓存应该尽量快，所以代码量因保持最少;
- 一致性。缓存框架 API 提供跨越不同缓存后端的接口保持一致;
- 可扩展性。

django 内置了缓存框架，并支持以下常用的缓存后端:

- 使用 Memcached 缓存;
- 使用 MySQL 数据库进行缓存;
- 使用文件系统进行缓存;
- 使用本地内存进行缓存;
- 提供缓存扩展接口。

### 1.1 缓存后端配置

#### 1.1.1 Mysql 缓存配置

1. 创建缓存表:

  ```python
  python manage.py createcachetable cache_table
  ```

  此表有 cache_key, value, expires 三个字段，
2. 在 settings 中配置缓存:

  ```python
  CACHES = {
      'default': {
          'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
          'LOCATION': 'cache_table',
          'TIMEOUT': 60,
      }
  }
  ```

#### 1.1.2 Redis 缓存配置

官方没有实现 Redis 做缓存，但有开发者针对 django 开发了 Redis 缓存，有以下两种:

- `django-redis`: [官方文档](https://django-redis-chs.readthedocs.io/zh_CN/latest/)
- `django-redis-cache`: [官方文档](https://django-redis-cache.readthedocs.io/en/latest/)

这两种实现的配置有稍许不同，本次使用 django-redis，简单配置为:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

详细配置见官方文档的说明。

#### 1.1.3 多缓存

django 支持多缓存，在 CACHES 下添加并设置不同名称即可，使用时通过 `caches['cachename']` 来指定。如配置为:

```python
CACHES = {
    'default': {
          'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
          'LOCATION': 'cache_table',
          'TIMEOUT': 60,
    },
    "redis_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
```

### 1.2 视图中使用缓存

#### 1.2.1 缓存对象简介

缓存对象获取:

- 单缓存:

  ```python
  from django.core.cache import cache
  ```

- 多缓存:

  ```python
  from django.core.cache import caches
  cache = caches['cache_name']
  ```

缓存对象支持以下操作(按使用频率倒序):

- `set(key, value, timeout)`: 设置缓存，timeout 单位为秒，如果未指定，则使用 settings 中配置;
- `get(key)`: 获取缓存;
- `delete(key)`: 删除缓存;
- `clear()`: 清空所有缓存;
- `add(key, value, timeout)`: 同 `set`，但其会返回成功标志位;
- `get_or_set(key, value, timeout)`: 如果存在 key 则 get, 否则 set;
- `get_many(keys)`: 获取多个缓存;
- `set_many(data, timeout)`: 添加多个缓存，data 为字典;
- `delete_many(keys)`: 删除多个;
- `incr(key, delta=1)`: 计数缓存加;
- `decr(key, delta=1)`: 计数缓存减;

#### 1.2.2 装饰器使用缓存

从 `django.views.decorators.cache` 中导入 `cache_page`，在需要缓存的视图上添加装饰器即可。其有三个参数:

- 位置参数: 以秒为单位设定缓存过期时间，此参数为必须参数;
- cache: 关键字参数，多缓存后端配置，默认为 default;
- key_prefix: 关键字参数，key 的前置字符串

>例子:
>
>```python
>@cache_page(30)
>def cachedemo(request: HttpRequest):
>
>    messages = [i for i in range(10)]
>    time.sleep(3)  # 模拟速度慢
>    data = {
>        'messages': messages
>    }
>
>    return render(request, 'app_cacheDemo.html', context=data)
>```

#### 1.2.3 手动使用缓存

1. 如果缓存是全局使用（不区分客户端），则 key 可以为固定字符串，如果要区分客户端，则 key 应加入用户唯一标识，如 cookie 等等;
2. 视图内顶部获取缓存，如果获取到缓存则直接返回;
3. 如果未获取到缓存，则将 reponse.content 存入缓存。

>例子:
>
>```python
>def cachedemo(request: HttpRequest):
>    # 1. 获取缓存，成功获取则直接返回
>    result = cache.get('cachedemo')
>    if result:
>        return HttpResponse(result)
>
>    messages = [i for i in range(10)]
>    time.sleep(3)  # 模拟速度慢
>    data = {
>        'messages': messages
>    }
>
>    response = render(request, 'app_cacheDemo.html', context=data)
>
>    # 2. 设置缓存
>    cache.set('cachedemo', response.content, timeout=60)
>
>    return response
>```

## 2. 中间件

### 2.1 中间件简介

中间件: 轻量级、底层的插件，可以介入 django 请求和响应过程（面向切面编程），可介入的入口称为切点。中间件其本质是 Python 的类，通过装饰器来介入请求和响应过程。

> 面向切面编程(Aspect Oriented Programming, AOP)，主要目的是在切点处介入处理过程，它所面对的是处理过程中的某个步骤或者过程，以获得逻辑各部分的低耦合隔离效果。

### 2.2 中间件定义和启用示例

定义流程:

1. 在工程根目录创建 middleware 目录;
2. 目录中创建 python 脚本，写入中间件实现。如新写法:

    ```python
    from django.utils.deprecation import MiddlewareMixin
    from django.http import HttpRequest


    class OldStyleAOP(MiddlewareMixin):
        ''' 旧写法 '''
        def process_request(self, request: HttpRequest):
            ''' url 解析之前 '''
            print(f'\nrequest: {self.process_request.__doc__}')
            print('old style - user ip:', request.META.get('REMOTE_ADDR'))
    ```

4. 启用中间件：在 setting 的中间件注册列表 *MIDDLEWARE* 中添加 `目录.文件名.类名`，如本次为 `'middleware.newstyleAOP.NewStyleAOP'`，这样就会作用在所有请求-响应过程中。

### 2.3 中间件切点

Django 1.10之后，正式推出中间件的新版本，关于新版本官方文档 [middleware](https://docs.djangoproject.com/en/1.10/topics/http/middleware/#writing-your-own-middleware)。旧写法仍然在后续版本可以使用，django 会通过 `django.utils.deprecation.MiddlewareMixin` 将旧写法转化为新写法。(查看了目前最新的 3.0.6 版本，自带的中间件仍然使用旧写法，故本文也使用旧写法)。

Django 内置切点:

- `init`: 无参数，旧版本(<1.10)为服务响应第一个请求时被调用，新版本为服务启动时调用;
- `process_request(self, request)`: 在接收到请求，URL 还未解析时调用。即每个请求都会调用，不主动返回;
- `process_view(self, request, view_func, view_args, view_kargs)`: 在解析了 URL 确定了视图函数后，调用视图之前被调用，每个请求都会调用，不主动返回;
- `process_template_response(self, request, response)`: 如果视图函数返回实例有 render 方法，则在视图执行完成后立即执行，不主动返回。其返回对象也必须实现 render，~~可以通过修改 response.template_name 和 response.context_data 来返回新的响应~~(测试发现并没有相关属性？);
- `process_exception(self, request, exception)`: 视图或者template_response抛出异常时调用，不主动返回;
- `process_response(self, request, response)`: 响应返回到浏览器前调用，不主动返回，注意此切点实际中必须要返回，否则那就会导致请求中断。

上面切点如果返回了 HttpResponse，则就会直接返回给浏览器，后续的都不会执行；如果不返回或者返回 None，执行完后会接着正常执行后续，如下图 1 所示：

![django中间件切点示意图](/md_img/005_Cache-Middleware.assets/django中间件切点示意图.png)
(*figure 1*)

旧写法示例:

```python
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse


class OldStyleAOP(MiddlewareMixin):
    ''' 旧写法 '''
    def __init__(self, get_response=None):
        ''' 在 Web 启动时执行，参数只能传 get_response '''
        super().__init__(get_response=get_response)
        print(f'\n\nfirst: {self.__init__.__doc__}')

    def process_request(self, request: HttpRequest):
        ''' url 解析之前 '''
        print(f'\nrequest: {self.process_request.__doc__}')
        print('old style - user ip:', request.META.get('REMOTE_ADDR'))

    def process_view(self, request, view_func, view_args, view_kargs):
        ''' url 解析之后，进入 view 之前 '''
        print(f'view: {self.process_view.__doc__}')

    def process_template_response(self, request, response):
        ''' view 返回对象包含 render 方法时调用，此返回也必须包含 render '''
        print(f'templates: {self.process_template_response.__doc__}')
        # raise Exception('exception in process_template_response')

    def process_exception(self, request, exception):
        ''' view 或 template_response 发生异常时调用 '''
        print(f'---exception---: {self.process_exception.__doc__}')

    def process_response(self, request: HttpRequest, response):
        ''' 返回浏览器前调用，必须有返回 '''
        print(f'response: {self.process_response.__doc__}')
        return HttpResponse('response')
```

新写法示例:

```python
from django.http import HttpRequest


class NewStyleAOP(object):
    def __init__(self, get_response):
        ''' 在 Web 启动时执行，参数只能传 get_response '''
        self.get_response = get_response
        print(f'\n\nfirst: {self.__init__.__doc__}')

    def __call__(self, request: HttpRequest):
        '''每个请求-响应流程均会执行
        '''
        # 到达 view 之前执行，即相当于 process_request
        print(f'new style - user ip: {request.META.get("REMOTE_ADDR")} \n')

        response = self.get_response(request)  # 获取 view 和其他中间件的返回

        # 返回浏览器前执行，相当于 process_response

        return response

    def process_view(self, request, view_func, view_args, view_kargs):
        ''' url 解析之后，进入 view 之前 '''
        print(f'view: {self.process_view.__doc__}')

    def process_template_response(self, request, response):
        ''' view 返回对象包含 render 方法时调用，此返回也必须包含 render '''
        print(f'templates: {self.process_template_response.__doc__}')
        # raise Exception('exception in process_template_response')

    def process_exception(self, request, exception):
        ''' view 或 template_response 发生异常时调用 '''
        print(f'---exception ---\n: {self.process_exception.__doc__}')
```

### 2.4 中间件执行顺序

单个中间件顺序如上 #2.3 图 1 所示。
多个中间件调用顺序:

- 按照中间件注册列表顺序从上到下一次执行
- 如果某个中间件进行了返回，则后续中间件不在执行

### 2.5 中间件应用

- 统计功能
  - 统计 ip
  - 统计浏览器
- 权重控制
  - 白名单
  - 黑名单
- 反爬
  - 访问间隔
  - 频率控制
- CSRF

如下例:

```python
class AopDemo(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR')

        if request.path == '/appmw/index/':
            # 权重优先级控制
            if ip == '127.0.0.1':
            # if ip.startswith('127.0.0.'):
                if random.randrange(10) > 2:
                    return HttpResponse('成功')
                else:
                    return HttpResponse('下次一定')

        if request.path == '/appmw/testaop1/':
            # 反爬 1：访问间隔
            cache = caches['redis_cache']
            result = cache.get(ip)  # 此处实验使用 ip 作为 key

            if result:
                return HttpResponse('十秒内只能访问一次。')
            cache.set(ip, True, 10)

        if request.path == '/appmw/testaop2/':
            # 反爬 2: 频率控制，时间段 m 秒内只能访问 n 次
            m, n = 15, 3
            cache = caches['redis_cache']
            request_ts = cache.get(ip, [])  # 此处实验使用 ip 作为 key

            now = time.time()
            request_ts.insert(0, now)

            while request_ts and (now - request_ts[len(request_ts) - 1]) > m:
                request_ts.pop()
            if len(request_ts) > n:
                return HttpResponse(f'{m}秒内只能访问{n}次，稍后再试')

            cache.set(ip, request_ts)
```

CSRF 实现机制见下篇。
