from django_crontab_manager.models import Cronjob
from .repository import DjangoRepository


class CronjobRepository(DjangoRepository):
    def __init__(self) -> None:
        super().__init__(Cronjob)

    def create(self, jobhash, setting):
        return Cronjob.objects.get_or_create(jobhash=jobhash, setting=setting)[0]

