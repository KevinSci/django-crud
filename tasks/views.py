from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save() 
                login(request, user)
                return redirect('tasks')               
            except IntegrityError:
                return render(request, 'sign-up.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe',
                })
        return render(request, 'sign-up.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no son las mismas'
        })
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # filtradas por nombre del usuario actual
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create-task.html', {
            'form': TaskForm
        })
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')

@login_required
def sing_out(request):
    logout(request)
    return redirect('home')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'sign-in.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')
        
        
@login_required        
def task(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task.html', {'task': task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'task.html', {'task': task, 'form':form, 'error': 'Error al actualizar'})


@login_required
def task_complete(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

    
@login_required    
def task_delete(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')