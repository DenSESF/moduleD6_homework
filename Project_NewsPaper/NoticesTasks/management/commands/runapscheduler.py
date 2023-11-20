from django.core.management.base import BaseCommand
from NoticesTasks.scheduler import bl_notice_tasks_scheduler


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        bl_notice_tasks_scheduler()
