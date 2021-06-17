""" Raw views """

from django.urls import reverse
from django.views import View

from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponseRedirect,
    Http404
)

from ..forms import TaskForm, RawTaskForm
from ..models import Task

class TaskObjectMixin(object):
    model = Task
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class TaskListRawView(View):
    template_name = "task/task_list.html"
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        view_context = {
            "object_list": [task for task in Task.objects.all()]
        }
        return render(request, self.template_name, view_context)


class TaskCreateRawView(View):
    template_name = "task/task_create.html" # DetailView
    def get(self, request, *args, **kwargs):
        # GET method
        form = TaskForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("task:index"))
        context = {"form": form}
        return render(request, self.template_name, context)


class TaskUpdateRawView(TaskObjectMixin, View):
    template_name = "task/task_create.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = TaskForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = TaskForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()            
            return HttpResponseRedirect(reverse("task:detail", kwargs={"id": obj.id}))        


class TaskDeleteRawView(TaskObjectMixin, View):
    template_name = "task/task_delete.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method        
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()            
            return  HttpResponseRedirect(reverse('task:index'))
        return render(request, self.template_name, context)


class TaskDetailRawView(TaskObjectMixin, View):
    template_name = "task/task_detail.html" # DetailView    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        view_context = {            
            "object": self.get_object()
        }
        return render(request, self.template_name, view_context)