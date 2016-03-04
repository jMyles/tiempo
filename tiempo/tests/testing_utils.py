from twisted.trial.unittest import TestCase
from tiempo import TIEMPO_REGISTRY
from tiempo.conn import REDIS
from tiempo.runner import Runner
from tiempo.tests.sample_tasks import some_callable
from tiempo.utils.premade_decorators import hourly_task


class OneRunnerTestCase(TestCase):

    def setUp(self):
        super(OneRunnerTestCase, self).setUp()
        REDIS.flushall()
        self.runner = Runner(0, [1])

    def tearDown(self):
        self.runner.shut_down()
        REDIS.flushall()
        TIEMPO_REGISTRY.clear()
        super(OneRunnerTestCase, self).tearDown()

    def make_task_and_job_for_runner(self):
        task = hourly_task(some_callable)
        job = task.spawn_job_and_run_soon()
        d = self.runner.cycle()
        return d
