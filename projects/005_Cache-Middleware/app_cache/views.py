from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from django.views.decorators.cache import cache_page
# from django.core.cache import cache
from django.core.cache import caches


def index(request):
    return HttpResponse('app cache index')


# @cache_page(30)
def cachedemo(request: HttpRequest):
    cache = caches['redis_cache']
    # 1. 获取缓存，成功获取则直接返回
    result = cache.get('cachedemo')
    if result:
        return HttpResponse(result)

    messages = [i for i in range(10)]
    time.sleep(3)  # 模拟速度慢
    data = {
        'messages': messages
    }

    response = render(request, 'app_cacheDemo.html', context=data)

    # 2. 设置缓存
    cache.set('cachedemo', response.content, timeout=60)

    return response
