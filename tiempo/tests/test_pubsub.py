from twisted.trial.unittest import TestCase
import time
from twisted.internet import task
from tiempo.conn import REDIS, hear_from_backend, subscribe_to_backend_notifications

parse_backend = hear_from_backend()

class EventsBroadCastTests(TestCase):

    def test_subscribing_causes_notifications(self):
        REDIS.flushall()
        REDIS.config_set('notify-keyspace-events', '')
        REDIS.config_get('notify-keyspace-events')
        # Notifications are now turned off.

        # However, subscribing turns them back on.
        subscribe_to_backend_notifications()
        config = REDIS.config_get('notify-keyspace-events')
        self.assertEqual(config['notify-keyspace-events'], 'AKE')

    def test_subscribe_notice(self):
        REDIS.flushall()
        subscribe_to_backend_notifications()
        time.sleep(.1)

        parse_backend()
        parse_backend()
        parse_backend()
        event_list = parse_backend()
        subscribe_event = event_list.pop()
        self.assertEqual(subscribe_event['type'], 'psubscribe')

    def test_result_is_properly_reported(self):
        REDIS.flushall()
        subscribe_to_backend_notifications()

        REDIS.set('results:whatever', 'a large farva')

        parse_backend()
        parse_backend()
        parse_backend()
        event_list = parse_backend()
        for event in event_list:
            key = event['channel'].split(':', 1)[1]
            new_value = REDIS.get(key)
            if new_value == 'a large farva':
                self.assertEqual(new_value, 'a large farva')

    def teardown(self):
        REDIS.flushall()
