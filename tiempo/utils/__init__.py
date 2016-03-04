import datetime
import importlib
import os
from collections import OrderedDict

import chalk
import pytz
from django.utils import six

from tiempo.conf import TASK_PATHS
from tiempo.conn import REDIS


def utc_now():
    return datetime.datetime.now(pytz.utc)


def import_tasks():
    for app in TASK_PATHS:
        if not app.split('.')[-1] == 'tasks':
            module = importlib.import_module(app)
            filename = os.path.join(module.__path__[0], 'tasks.py')
            if not os.path.isfile(filename):
                chalk.yellow(app + ' does not have a tasks module.')
                continue
            else:
                app = app + '.tasks'

        chalk.blue(app.upper() + ': imported tasks from %s' % app)
        importlib.import_module(app)


# /////////////////////////////////////////////////////////////////////////////
# Django Rubbish
class Promise(object):
    """
    This is just a base class for the proxy class created in
    the closure of the lazy function. It can be used to recognize
    promises in code.
    """
    pass


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, six.memoryview):
        s = bytes(s)
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if isinstance(s, Promise):
        return six.text_type(s).encode(encoding, errors)
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join(
                    [
                        force_bytes(arg, encoding, strings_only, errors)
                        for arg in s
                    ]
                )
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)


def namespace(group_name):
    if group_name:
        return '%s:%s' % (REDIS_GROUP_NAMESPACE, group_name)

    # returns None if passed something Falsey.


def all_jobs(groups):
    '''
    Find all Jobs in the list of groups, return them as a dict.
    '''
    jobs_dict = OrderedDict()
    for group in groups:
        name = namespace(group)
        jobs_dict[group] = REDIS.lrange(name, 0, -1)
    return jobs_dict


class JobReport(object):

    def __init__(self, groups_list=None):
        self.groups = groups_list if groups_list else all_task_groups()

    def __getitem__(self, slice):
        if slice.step:
            raise TypeError("JobReport can't be sliced for step with this backend.")
        keys = REDIS.zrange("all_results", slice.start or 0, slice.stop or -1)
        pipe = REDIS.pipeline()
        for key in keys:
            pipe.hgetall(key)
        results = pipe.execute()
        return results