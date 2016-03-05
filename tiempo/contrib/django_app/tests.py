from rest_framework.test import APISimpleTestCase

from tiempo.tests.testing_utils import OneRunnerTestCase


class JobHistoryApiTests(APISimpleTestCase, OneRunnerTestCase):

    def test_51_jobs_paginated(self):
        d = self.make_task_and_job_for_runner()

        def api_examination(*args):
            response = self.client.get('/api/v1/jobs/')
            self.assertEqual(self.runner.current_job.uid, response.data['results'][0]['jobUid'])
        d.addCallback(api_examination)
        return d