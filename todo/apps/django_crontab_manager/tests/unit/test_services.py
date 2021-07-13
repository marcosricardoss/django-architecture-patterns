import pytest
from django_crontab_manager.adapters import executor
from typing import List

from django_crontab_manager.models import Cronjob
from django_crontab_manager.adapters import AbstractExecutor, AbstractRepository
from django_crontab_manager.adapters import AbstractExecutor
from django_crontab_manager.services import (
    add_all_cronjobs,
    get_cronjob_from_settings,
    load_cronjobs_to_db,
    remove_all_cronjobs,
    run_cronjob,
)
from django_crontab_manager.app_settings import CRONJOBS

class FakeRepository(AbstractRepository):
    def __init__(self, Model: object) -> None:
        self.deleted = False
        self.data = [
            ("jobhash1", "setting1"),
            ("jobhash2", "setting2"),
            ("jobhash3", "setting3"),
        ]
        self.created_data = []

    def get(self):
        pass

    def list(self) -> List[object]:
        return self.data

    def delete(self) -> None:
        self.deleted = True


class FakeCronjobRepository(FakeRepository):
    def create(self, jobhash, setting):
        self.created_data.append((jobhash, setting))


class FakeExecutor(AbstractExecutor):
    def __init__(self) -> None:
        self.commands = None

    def run(self, commands):
        self.commands = commands


def test_get_cronjob_from_settings_service():
    cronjobs = get_cronjob_from_settings()
    assert list(cronjobs.values()) == CRONJOBS


def test_run_cronjob_service():
    executor = FakeExecutor()
    run_cronjob("xxxxxxxx", executor)
    assert executor.commands == ["crontab", "run", "xxxxxxxx"]


def test_add_all_cronjobs_service():
    executor = FakeExecutor()
    add_all_cronjobs(executor)
    assert executor.commands == ["crontab", "add"]


def test_add_all_cronjobs_service():
    executor = FakeExecutor()
    add_all_cronjobs(executor)
    assert executor.commands == ["crontab", "add"]


def test_remove_all_cronjobs_service():
    executor = FakeExecutor()
    remove_all_cronjobs(executor)
    assert executor.commands == ["crontab", "remove"]


def test_load_cronjobs_to_db():
    repository = FakeCronjobRepository(object)
    load_cronjobs_to_db(repository)
    assert repository.deleted
    assert repository.data == repository.created_data