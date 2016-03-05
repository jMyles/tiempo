#! python

import os, sys
import tiempo
tiempo.LEAVE_DJANGO_UNSET = True

from tiempo import conf
conf.REDIS_QUEUE_DB = conf.REDIS_TEST_DB

# begin chdir armor
sys.path[:] = map(os.path.abspath, sys.path)
# end chdir armor

sys.path.insert(0, os.path.abspath(os.getcwd()))
sys.argv.append("tiempo/tests")

####

# And now the django part.
def run_django_tests():
    import django
    from django.conf import settings
    from django.test.utils import get_runner

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


    def run_settings():
        settings.configure(
            MIDDLEWARE_CLASSES=[],
            ROOT_URLCONF='tiempo.contrib.django_app.urls',
            TIEMPO_MANUAL=True,
            INSTALLED_APPS=[
                'tiempo.contrib.django_app',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                ],
            SECRET_KEY = "LLAMAS",

            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            },
        )

    run_settings()
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    django_test_results = test_runner.run_tests(["tiempo.contrib.django_app"])
    return django_test_results


try:
    from twisted.scripts.trial import run
    run()
except SystemExit as finished_trial_run:
    trial_failed = bool(finished_trial_run)
finally:
    django_test_results = run_django_tests()
    django_tests_failed = bool(django_test_results)
    sys.exit(trial_failed or django_tests_failed)
