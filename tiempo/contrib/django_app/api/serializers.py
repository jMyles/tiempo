from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from tiempo.utils import JobReport


class JobsPaginator(LimitOffsetPagination):

    default_limit = 50
    offset = 0

    def __init__(self, *args, **kwargs):
        super(JobsPaginator, self).__init__(*args, **kwargs)

    def get_paginated_response(self, data):
        return super(JobsPaginator, self).get_paginated_response(data)


class JobSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return obj
