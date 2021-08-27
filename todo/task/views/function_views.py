""" Functions based Views """

from django.urls import reverse
from django.shortcuts import Http404, HttpResponseRedirect, get_object_or_404, render

from task.forms import TaskForm, RawTaskForm
from task.models import Task


def list_view(request, *args, **kwargs):  # pragma: no cover
    """ """
    view_context = {"object_list": [task for task in Task.objects.all()]}
    return render(request, "task/task_list.html", view_context)


def create_view(request, *args, **kwargs):  # pragma: no cover
    """Using built-in django form"""

    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("task:index"))

    view_context = {"form": form}
    return render(request, "task/task_create.html", view_context)


def create_view_raw(request, *args, **kwargs):  # pragma: no cover
    """Creating a raw django form"""

    if request.method == "POST":
        form = RawTaskForm(request.POST)
        if form.is_valid():
            Task.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse("task:index"))
        else:
            print(form.errors)
    elif request.method == "GET":
        form = RawTaskForm()
        view_context = {"form": form}
        return render(request, "task/task_create.html", view_context)

    Http404()


def update_view(request, id, *args, **kwargs):  # pragma: no cover
    """Using built-in django form"""

    # # Option 1
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task. DoesNotExist:
    #     raise Http404

    # # Option 2
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task.DoesNotExist:
    #     return HttpResponseNotFound("Not found")

    # Option 3
    obj = get_object_or_404(Task, id=id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(obj.get_absolute_url())
    elif request.method == "GET":
        form = TaskForm(None, instance=obj)
        view_context = {"form": form}
        return render(request, "task/task_create.html", view_context)

    Http404()


def delete_view(request, id, *args, **kwargs):  # pragma: no cover
    """ """

    # # Option 1
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task. DoesNotExist:
    #     raise Http404

    # # Option 2
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task.DoesNotExist:
    #     return HttpResponseNotFound("Not found")

    # Option 3
    obj = get_object_or_404(Task, id=id)

    if request.method == "POST":
        obj.delete()
        print(reverse("task:index"))
        return HttpResponseRedirect(reverse("task:index"))
    elif request.method == "GET":
        view_context = {"object": obj}
        return render(request, "task/task_delete.html", view_context)

    Http404()


def detail_view(request, id, *args, **kwargs):  # pragma: no cover
    """ """

    # # Option 1
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task. DoesNotExist:
    #     raise Http404

    # # Option 2
    # try:
    #     obj = Task.objects.get(id=id)
    # except Task.DoesNotExist:
    #     return HttpResponseNotFound("Not found")

    # Option 3
    obj = get_object_or_404(Task, id=id)

    view_context = {"object": obj}
    return render(request, "task/task_detail.html", view_context)
