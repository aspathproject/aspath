from celery import Celery
from celery.schedules import crontab
from grabber_run import grab_new_datasets
from ingester_run import ingest_pending_snapshots

app = Celery('worker', backend='redis://redis:6379', broker='redis://redis:6379/0')
app.conf.update(CELERY_REDIS_SCHEDULER_URL = 'redis://redis:6379')
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  return

@app.task
def grab_and_ingest(collector_name):
    print(f"Starting grabber for collector {collector_name}")
    grab_new_datasets(collector_name)
    print(f"Starting ingestion process for collector {collector_name}")
    ingest_pending_snapshots(collector_name)
