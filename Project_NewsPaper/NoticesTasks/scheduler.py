import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from NoticesTasks.tasks import (
    testing_job,
    delete_old_job_executions,
    now_notice_create_post,
    week_notice_added_new_posts,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# for key in logging.Logger.manager.loggerDict:
#     print(key)
logging.getLogger('apscheduler').setLevel(logging.WARNING)


def bg_notice_create_new_post(fields):
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
  
    scheduler.add_job(
        now_notice_create_post,
        args=[fields]
    )
    logger.info("Added job 'bg_now_notice_create_post'.")

    logger.info("Starting scheduler...")
    scheduler.start()


def bl_notice_tasks_scheduler():
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    scheduler.add_job(
        testing_job,
        trigger=CronTrigger(minute="*/5"
        ),
        id="testing_job",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'testing_job'.")

    scheduler.add_job(
        week_notice_added_new_posts,
        trigger=CronTrigger(
            day_of_week="mon",
            # hour="10",
            minute="*/1",
        ),
        id="week_notice_add_new_post",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job 'week_notice_add_new_post'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
