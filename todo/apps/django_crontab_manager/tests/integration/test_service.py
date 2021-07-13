from django_crontab_manager.adapters import DjangoExecutor
from django_crontab_manager.services import (
    add_all_cronjobs,   
    get_cronjob_running, 
    remove_all_cronjobs,
)

def test_run_cronjob_service():
    executor = DjangoExecutor()
    
    add_all_cronjobs(executor)
    jobs_running = get_cronjob_running()
    assert jobs_running

    remove_all_cronjobs(executor)
    jobs_running = get_cronjob_running()
    assert not jobs_running


