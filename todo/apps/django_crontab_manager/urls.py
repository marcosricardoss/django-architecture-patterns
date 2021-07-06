from django.urls import path


app_name = "django_crontab_manager"

from .views import (
    CronJobHomeView,    
    AddAllCronJobsView,
    RemoveAllCronJobsView,        
    RunCronJobView,
)

urlpatterns = [
    path("", CronJobHomeView.as_view(), name="home"),    
    path("add/", AddAllCronJobsView.as_view(), name="add"),    
    path("remove/", RemoveAllCronJobsView.as_view(), name="remove"),    
    path("run/<str:jobhash>/", RunCronJobView.as_view(), name="run"),
]
