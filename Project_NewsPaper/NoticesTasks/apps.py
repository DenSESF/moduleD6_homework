from django.apps import AppConfig


class NoticestasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NoticesTasks'

    def ready(self) -> None:
            import NoticesTasks.signals
            return super().ready()
