""" Classes based Views """

from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView    
)
from django.shortcuts import (
    get_object_or_404,
    HttpResponseRedirect,
    Http404
)

from ..forms import TaskForm, RawTaskForm
from ..models import Task

class TaskListView(ListView):
    """ ListView """
    
    template_name = "task/task_list.html"
    queryset = Task.objects.all()


class TaskCreateView(CreateView):
    """ CreateView """

    template_name = "task/task_create.html"
    form_class = TaskForm
    queryset = Task.objects.all()

    # Change the success url. If there's a get_absolute_url()
    # method in the model this will be ignored.
    # success_url = "/"

    def form_valid(self, form):
        """ DetailView.get_object() method """

        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Another way to change the success url. If there's a
        get_absolute_url() method in the model this will be ignored.
        """    
        return reverse('task:index')        


class TaskUpdateView(UpdateView):
    """ UpdateView """

    template_name = "task/task_create.html"
    form_class = TaskForm        

    def form_valid(self, form):
        """ DetailView.get_object() method """

        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self):
        """ 
        Overwrite UpdateView get_object() method        
        to get the 'id' argument instead of 'pk' 
        default argument. 
        """

        _id = self.kwargs.get("id")        
        return get_object_or_404(Task, id=_id)     


class TaskDeleteView(DeleteView):
    """ DeleteView """

    template_name = "task/task_delete.html"

    def get_object(self):
        """ 
        Overwrite UpdateView get_object() method        
        to get the 'id' argument instead of 'pk' 
        default argument. 
        """

        _id = self.kwargs.get("id")
        return get_object_or_404(Task, id=_id)        

    def get_success_url(self):
        return reverse('task:index')
        

class TaskDetailView(DetailView):
    """ DetailView """

    template_name = "task/task_detail.html"    

    def get_object(self):
        """ 
        Overwrite UpdateView get_object() method        
        to get the 'id' argument instead of 'pk' 
        default argument. 
        """
    
        _id = self.kwargs.get("id")
        return get_object_or_404(Task, id=_id)