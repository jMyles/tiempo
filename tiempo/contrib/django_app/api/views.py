from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from tiempo.contrib.django_app.api.serializers import JobSerializer
from tiempo.utils import JobReport


class TiempoHistoryViewSet(viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = JobSerializer

    def list(self, request):
        jobs = JobReport()[:50]
        return self.get_serializer(jobs, many=True)


