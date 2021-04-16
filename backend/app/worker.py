from celery import Celery
from celery.schedules import crontab

app = Celery('worker', backend='redis://redis:6379', broker='redis://redis:6379/0')
app.conf.update(CELERY_REDIS_SCHEDULER_URL = 'redis://redis:6379')
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(3600.0, test.s('alive check'), name='add every 3600')

    sender.add_periodic_task(
        crontab(hour=6, minute=30),
        test.s('TODO: execute daily PCH grabber here'),
    )

@app.task
def test(arg):
    print(arg)
