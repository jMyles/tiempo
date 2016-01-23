import datetime

from twisted.trial.unittest import TestCase
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from tiempo import TIEMPO_REGISTRY
from tiempo.conn import REDIS
from tiempo.work import Trabajo, Job
from tiempo.tests.sample_tasks import some_callable
from tiempo.insight import completed_jobs
from tiempo.runner import Runner

class RunnerTests(TestCase):
    """
    Tests for Tiempo's Runner class
    """
    decorated = Trabajo()(some_callable)
    simple_job = decorated.just_spawn_job()
    runner = Runner(0, [1])

    def setup(self):
        TIEMPO_REGISTRY.clear()
        REDIS.flushdb()
        reactor.run()

    def test_action_time_is_datetime(self):
        self.assertIsInstance(self.runner.action_time, datetime.datetime)

    def test_runner_is_busy(self):
        job = self.simple_job.soon()
        result = self.runner.cycle()
        self.assertIsInstance(result, Deferred)
        self.assertEqual(self.runner.cycle(), 500)
        self.assertEqual(self.runner.cycle(), 500)
        result.addCallback(self.runner.cleanup)
        self.runner.run()
        return

    def test_runner_cleanup(self):
        def check(result):
            self.assertEqual(self.runner.currenct_job, None)
            self.assertEqual(self.runner.start_time, None)
            self.assertEqual(self.runner.finish_time, None)
            self.assertEqual(self.runner.error_state, False)
        job =self.simple_job.soon()
        result = self.runner.cycle()
        self.assertIsInstance(result, Deferred)
        result.addCallbacks(self.runner.cleanup)
        result.addCallback(check)
        return
