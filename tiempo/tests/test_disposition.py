from tiempo.conn import REDIS
from tiempo.tests.sample_tasks import some_callable
from tiempo.tests.testing_utils import OneRunnerTestCase
from tiempo.utils.premade_decorators import hourly_task


class SuccessAndErrorsTests(OneRunnerTestCase):

    def test_runner_success(self):
        task = hourly_task(some_callable)
        self.runner.current_job = task.just_spawn_job()
        self.runner.announcer = self.runner.current_job.announcer
        test_message = "this message was generated during the run."
        self.runner.announcer.brief(test_message)
        backend_response = self.runner.handle_success(None)
        self.assertEqual(backend_response, [1, 1, True])  # Two 1s, each for pushing one entry to our sorted sets, and one True, for pushing the hash.

        # So, at this point, we expect the success to have been saved in the backend.
        # First, we use the key of the task to get the redis key to a hash of our results.
        hash_key = REDIS.zrange("results:%s" % self.runner.current_job.task.key, 0, 0)[0]

        # Now that we have the hash key, we can get the details of the run.
        job_report = REDIS.hgetall(hash_key)
        self.assertIn(test_message, job_report['result'])  # TODO: Why isn't this actually the string?  Why 'in'?