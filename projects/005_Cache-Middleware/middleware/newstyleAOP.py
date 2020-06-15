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
