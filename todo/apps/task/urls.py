from django.urls import path


app_name = 'task'

#########################################################
# Raw views
#########################################################

from .views import (    
    TaskCreateRawView,
    TaskDeleteRawView,
    TaskDetailRawView,
    TaskListRawView,      
    TaskUpdateRawView  
)

urlpatterns = [
    path('', TaskListRawView.as_view(), name='index'),
    path('create/', TaskCreateRawView.as_view(), name='create'),
    path('update/<int:id>/', TaskUpdateRawView.as_view(), name='update'),
    path('delete/<int:id>/', TaskDeleteRawView.as_view(), name='delete'),
    path('detail/<int:id>/', TaskDetailRawView.as_view(), name='detail')    
]

# #########################################################
# # Classes based views
# #########################################################

# from .views (
#     TaskCreateView,
#     TaskDeleteView,
#     TaskDetailView,
#     TaskListView,
#     TaskUpdateView
# )

# urlpatterns = [
#     path('', TaskListView.as_view(), name='index'),
#     path('create/', TaskCreateView.as_view(), name='create'),
#     path('update/<int:id>/', TaskUpdateView.as_view(), name='update'),
#     path('delete/<int:id>/', TaskDeleteView.as_view(), name='delete'),
#     path('detail/<int:id>/', TaskDetailView.as_view(), name='detail')    
# ]

#########################################################
# Functions based Views
#########################################################

# from .views (     
#     list_view,
#     create_view, 
#     create_view_raw,
#     update_view ,
#     delete_view,
#     detail_view    
# )

# urlpatterns = [
#     path('', list_view, name='index'),
#     path('create/', create_view, name='create'),
#     path('createraw/', create_view_raw, name='createraw'),
#     path('update/<int:id>/', update_view, name='update'),
#     path('delete/<int:id>/', delete_view, name='delete'),
#     path('detail/<int:id>/', detail_view, name='detail')    
# ]