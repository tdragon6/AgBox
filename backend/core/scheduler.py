'''
定时任务调度器
'''


from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from core.config import settings

jobstores = {
    'default': SQLAlchemyJobStore(
        url=settings.DATABASE_URL,
        tablename='scheduler'
    )
}

executors = {
    'default': ThreadPoolExecutor(settings.SCHEDULER_MAX_JOBS)
}

job_defaults = {
    'coalesce': settings.SCHEDULER_COALESCE,
    'max_instances': settings.SCHEDULER_MAX_INSTANCES
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
)