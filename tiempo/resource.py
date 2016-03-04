from collections import OrderedDict
from hendrix.contrib.async.resources import MessageHandlerProtocol
from hendrix.contrib.async.messaging import hxdispatcher
import json


class TiempoMessageProtocol(MessageHandlerProtocol):

    def jobs_to_announce(self):
        # unsettings workaround
        from tiempo.utils import JobReport

        jobs = JobReport()[:50]
        return jobs

    def dataReceived(self, data):
        # Unsettings workaround
        from tiempo.insight import completed_jobs

        if data == "updateJobs":
            # TODO: Better way to announce jobs

            hxdispatcher.send('all_tasks', {'jobs': self.jobs_to_announce()})

            # All completed jobs. # TODO: Move these things to their own place.
            all_completed = completed_jobs()
            hxdispatcher.send('results', {'results': all_completed})
        else:
            return MessageHandlerProtocol.dataReceived(self, data)