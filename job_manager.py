from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import datetime as dt
from datetime import timedelta


def process_job():
    for number in range(1000000):
        print(number)


def processor_full():
    dti = pd.date_range('2018-01-01', periods=365, freq='D')
    value_data = range(365)
    dfData = pd.DataFrame(data={'datevalue': dti, 'value': value_data})
    dfData.index = dfData['datevalue']
    dfData = dfData['value']
    dfDataFrame = dfData.to_frame()
    current_time = dt.datetime.utcnow()
    end_time = current_time + timedelta(minutes=5)
    while end_time >= dt.datetime.utcnow():
        print(current_time)


def processor_crazy():
    dti = pd.date_range('2018-01-01', periods=365, freq='D')
    value_data = range(365)
    dfData = pd.DataFrame(data={'datevalue': dti, 'value': value_data})
    dfData.index = dfData['datevalue']
    dfData = dfData['value']
    dfDataFrame = dfData.to_frame()
    current_time = dt.datetime.utcnow()
    end_time = current_time + timedelta(minutes=30)
    while end_time >= dt.datetime.utcnow():
        print(current_time)


class JobManager(object):
    def __init__(self):
        jobstore = {
            'default': SQLAlchemyJobStore(url='sqlite:///job.db')
        }
        executors = {
            'default': ThreadPoolExecutor(100),
            'processpool': ProcessPoolExecutor(100)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 100
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstore, executors=executors, job_defaults=job_defaults, timezone=utc)
        self.scheduler.start()

    def add_crazy(self, job_id):
        get_all_job_names = self.get_all_jobs()
        if job_id not in get_all_job_names:
            job = self.scheduler.add_job(processor_crazy, 'interval', minutes=5, id=job_id)
            job.resume()

    def add_job(self, job_id):
        get_all_job_names = self.get_all_jobs()
        if job_id not in get_all_job_names:
            job = self.scheduler.add_job(processor_full, 'interval', minutes=5, id=job_id)
            job.resume()

    def add_low_usage_job(self, job_id):
        get_all_job_names = self.get_all_jobs()
        if job_id not in get_all_job_names:
            job = self.scheduler.add_job(process_job, 'interval', minutes=1, id=job_id)
            job.resume()

    def get_process(self):
        process_job()

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def pause_scheduler(self):
        self.scheduler.pause()

    def resume_scheduler(self):
        self.scheduler.resume()

    def shutdown_scheduler(self):
        self.scheduler.shutdown()

    def get_all_jobs(self):
        all_jobs = self.scheduler.get_jobs()
        return_jobs = []
        for single_job in all_jobs:
            return_jobs.append(single_job.id)
        return return_jobs

    def kill_scheduler(self):
        self.scheduler.shutdown(wait=False)
