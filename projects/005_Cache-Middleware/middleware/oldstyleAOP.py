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
        # print('old style - user ip:', request.META.get('REMOTE_ADDR'))
        print(f'\nrequest: {self.process_request.__doc__}')

    def process_view(self, request, view_func, view_args, view_kargs):
        ''' url 解析之后，进入 view 之前 '''
        print(f'view: {self.process_view.__doc__}')
        view_func(request, *view_args, **view_kargs)

    def process_template_response(self, request, response):
        ''' view 返回对象包含 render 方法时调用，此返回对象也必须包含 render 方法 '''
        print(f'templates: {self.process_template_response.__doc__}')
        # raise Exception('exception in process_template_response')

    def process_exception(self, request, exception):
        ''' view 或 template_response 发生异常时调用 '''
        print(f'---exception---: {self.process_exception.__doc__}')

    # def process_response(self, request: HttpRequest, response):
    #     ''' 返回浏览器前调用，必须有返回 '''
    #     print(f'response: {self.process_response.__doc__}')
    #     return HttpResponse('response')
