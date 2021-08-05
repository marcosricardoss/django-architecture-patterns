import os
import pytest

from datetime import timedelta

from selenium import webdriver

from django.core.management import call_command
from django.test import Client
from django.utils import timezone


@pytest.fixture
def dates():
    today = timezone.now()
    tomorrow = today + timedelta(days=1)
    later = tomorrow + timedelta(days=10)

    return {"today": today, "tomorrow": tomorrow, "later": later}


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "dumpdata.json")


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def browser():
    SELENIUM_URL = os.environ.get("SELENIUM_URL")
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL, options=chrome_options
    )
    yield driver
