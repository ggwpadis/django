from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    return render(request, 'crud/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'crud/task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:task_list')
    else:
        form = TaskForm()

    return render(request, 'crud/task_form.html', {
        'form': form,
        'page_title': 'Create task',
    })


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('crud:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'crud/task_form.html', {
        'form': form,
        'page_title': 'Edit task',
    })


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('crud:task_list')

    return render(request, 'crud/task_confirm_delete.html', {'task': task})