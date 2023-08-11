from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, "home.html")
def signup(request):
    print(request.method)
    if request.method == "GET":
        return render(request, "signup.html",{
        "form":UserCreationForm
    })
   
    if request.POST["password1"] == request.POST["password2"]:
        #   register user
        try:
            user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
            user.save()
            login(request,user)
            return redirect("tasks")
            
        except IntegrityError:
             return render(request, "signup.html",{
        "form":UserCreationForm,
        "error":"Username already exists"
    })      
    else:
        return render(request, "signup.html",{
        "form":UserCreationForm,
        "error":"Password do not match"
    }) 

def signin(request):
    if request.method == "GET":
        return render(request,"signin.html",{
        "form":AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request,"signin.html",{
        "form":AuthenticationForm,
        "error":"User or password is incorrect"
    })  
        else:
            login(request,user)
            return redirect("tasks")
            
@login_required
def signout(request):
    logout(request)
    return redirect("home")
@login_required
def create_task(request):
    if request.method == "GET":
        return render (request,"create_task.html",{
        "form":TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
             return render (request,"create_task.html",{
        "form":TaskForm,
        "error":"You have to provide valid data"
    })
@login_required
def tasks(request):
    # tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    print("tasksA VERDTE",tasks)
    if tasks:
        return render(request,"tasks.html",{
                "tasks":tasks
            })
    else:
        return render(request,"tasks.html",{
        "error":"No more tasks..." ,    
    })

    

@login_required
def task_detail(request,id):
    task = get_object_or_404(Task,pk=id)
      
    return render (request,"task_detail.html",{
        "task":task
    })

@login_required
def update_task(request,id):
    print(id)
    task = get_object_or_404(Task,id=id,user=request.user)

    if request.method == "GET":
        form = TaskForm(instance=task, initial={
            'title': task.title,
            'description': task.description,
            'important': task.important,
        })
        return render(request, "update_task.html", {
        "form": form,
    })
    else: 
        try :
            form = TaskForm(request.POST,instance=task)
            if form.is_valid:
                form.save()
                return redirect("/tasks")
        except ValueError:
            return render (request,"update_task.html",{
        "form":TaskForm,
        "error":"Error updating task"
    })
        
@login_required
def delete_task(request,id):
    try:
        task = get_object_or_404(Task,id=id)
        task.delete()
        return redirect("/tasks")
    except:
        return redirect("/tasks")
    
@login_required    
def task_completed(request,id):
    task = get_object_or_404(Task, pk=id)
    # task=Task.objects.get(id=id,user=request.user)
    try:
        if task.datecompleted is None:
            task.datecompleted = datetime.now()
        else:
            task.datecompleted = None
        task.save()
        return redirect("/tasks")
    except: 
        return redirect("/tasks")

@login_required
def all_tasks_performed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,"all_tasks_performed.html",{
        "tasks":tasks
    })