""" Raw views """

from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator


from utils.forms import DivErrorList

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404

from ..forms import TaskForm
from ..models import Task


class TaskObjectMixin(object):
    model = Task

    def get_object(self):
        id = self.kwargs.get("id")
        obj = None
        if id is not None:  # pragma: no cover
            obj = get_object_or_404(self.model, id=id)
        return obj


class TaskListRawView(View):
    template_name = "task/task_list.html"
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        task_list = Task.objects.all()
        paginator = Paginator(task_list, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        view_context = {"page_obj": page_obj}
        return render(request, self.template_name, view_context)


class TaskCreateRawView(View):
    template_name = "task/task_create.html"  # DetailView

    def get(self, request, *args, **kwargs):
        # GET method
        form = TaskForm(error_class=DivErrorList)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = TaskForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Task created successfully!")
            return HttpResponseRedirect(reverse("task:index"))
        context = {"form": form}
        return render(request, self.template_name, context)


class TaskUpdateRawView(TaskObjectMixin, View):
    template_name = "task/task_create.html"  # DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        form = TaskForm(instance=obj, error_class=DivErrorList)
        context["object"] = obj
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        # POST method
        obj = self.get_object()
        form = TaskForm(request.POST, instance=obj, error_class=DivErrorList)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Task updated successfully!")
        return HttpResponseRedirect(reverse("task:detail", kwargs={"id": obj.id}))


class TaskDeleteRawView(TaskObjectMixin, View):
    template_name = "task/task_delete.html"  # DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        obj = self.get_object()
        context = {"object": obj}
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        # POST method
        obj = self.get_object()
        obj.delete()
        messages.success(self.request, "Task deleted successfully!")
        return HttpResponseRedirect(reverse("task:index"))


class TaskDetailRawView(TaskObjectMixin, View):
    template_name = "task/task_detail.html"  # DetailView

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        view_context = {"object": self.get_object()}
        return render(request, self.template_name, view_context)
