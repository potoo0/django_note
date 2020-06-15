from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse
import random
from django.core.cache import caches
import time


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
            while request_ts and (now - request_ts[len(request_ts) - 1]) > m:
                request_ts.pop()

            request_ts.insert(0, now)
            cache.set(ip, request_ts)

            if len(request_ts) > n:
                return HttpResponse(f'{m}秒内只能访问{n}次，稍后再试')
