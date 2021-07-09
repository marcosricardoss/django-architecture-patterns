from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = "django_crontab_manager"

from .views import (
    CronJobHomeView,    
    AddAllCronJobsView,
    AddAllCronJobsAdminView,
    RemoveAllCronJobsView,        
    RemoveAllCronJobsAdminView,
    RunCronJobView,
)

urlpatterns = [
    path("", login_required(CronJobHomeView.as_view()), name="home"),    
    path("add/", login_required(AddAllCronJobsView.as_view()), name="add"),    
    path("add-admin/", login_required(AddAllCronJobsAdminView.as_view()), name="add-admin"),    
    path("remove/", login_required(RemoveAllCronJobsView.as_view()), name="remove"), 
    path("remove-admin/", login_required(RemoveAllCronJobsAdminView.as_view()), name="remove-admin"),        
    path("run/<str:jobhash>/", login_required(RunCronJobView.as_view()), name="run"),
    path("run-admin/<str:jobhash>/", login_required(RunCronJobView.as_view()), name="run"),
]