from apps.mainApp.models import Musician
from apps.mainApp.serializers import MusicianSerializer
from django.core.cache import cache
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
import redis
import time

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)


def log_db_queries(f):
    from django.db import connection

    def new_f(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        print("\n\n")
        print("-" * 80)
        print("db queries log for %s:\n" % f.__name__)
        print(" TOTAL COUNT : % s " % len(connection.queries))
        for q in connection.queries:
            print("%s: %s\n" % (q["time"], q["sql"]))
        end_time = time.time()
        duration = end_time - start_time
        print('\n Total time: {:.3f} ms'.format(duration * 1000.0))
        print("-" * 80)
        return res

    return new_f


class MusicianList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MusicianDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    @log_db_queries
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if serializer.data['id'] in cache:
            print('redis')
            queryset = cache.get(serializer.data['id'])
            return Response(queryset)
        else:
            print('db')
            cache.set(serializer.data['id'], serializer.data, timeout=60 * 2)
            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
