# Create your views here.
from django.views.generic import TemplateView
from django_sse.redisqueue import RedisQueueView

from socketio import socketio_manage
from myapp.namespaces import MyNamespace
from myapp.utils import redis_connection, emit_to_channel
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


class HomePage(TemplateView):
    template_name = 'index.html'


class SSE(RedisQueueView):
    pass


@csrf_exempt
def incr(request):
    r = redis_connection()
    count = r.incr('sheeple')
    emit_to_channel('default_room', 'myevent', count)
    return HttpResponse()


@csrf_exempt
def delete(request):
    r = redis_connection()
    r.delete('sheeple')
    emit_to_channel('default_room', 'myevent', 0)
    return HttpResponse()


def socketio_service(request):
    socketio_manage(request.environ, namespaces={'': MyNamespace}, request=request)

    return {}
