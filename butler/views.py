from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q,Count

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import employee,project,assignments,Task
from .forms import SignUpForm, UserForm, TaskForm, EmpForm, ProjectForm

# Index
@login_required(login_url='/login/')
def index(request):
  projCount = project.objects.count()
  completedTasks = Task.objects.filter(isCompleted=1).count()
  backlogTasks = Task.objects.filter(isCompleted=0).count()
  starEmployee = employee.objects.annotate(completed_tasks = Count('task',filter=Q(task__isCompleted=True))).order_by('-completed_tasks').first().empName
  leadEmployees = employee.objects.filter(project__projectLead__isnull=False).distinct()
  employees_with_backlog = (
    employee.objects
    .annotate(incomplete_tasks=Count('task', filter=Q(task__isCompleted=False))).order_by('-incomplete_tasks')
)
  DisplayData = {
      "projData":project.objects.all(),
      "empData":employee.objects.all(),
      "taskData":Task.objects.all(),
      "projCount" : projCount,
      "completedTasks":completedTasks,
      "backlogTasks":backlogTasks,
      "starEmployee":starEmployee,
      "leadEmployee":leadEmployees,
      "backLogEmployees":employees_with_backlog,

  }
  return render(request, 'pages/index.html',{"DisplayData":DisplayData})

@login_required(login_url='/login/')
def task_manager(request):
    TaskData = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task')
    else:
        form = TaskForm()

    
    return render(request,'pages/taskmanager.html',{"TaskData":TaskData,'form':form,"employees":employee.objects.all(),"projects":project.objects.all()})


@login_required(login_url='/login/')
def employee_manager(request):
    EmployeeData = employee.objects.all()
    if request.method == "POST":
        form = EmpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empMan')
    else:
        form = EmpForm()
    
    return render(request, 'pages/employeemanager.html', {"EmployeeData":EmployeeData,"form":form})

@login_required(login_url='/login/')
def project_manager(request):
    ProjectData = project.objects.all()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projMan')
    else:
        form = ProjectForm()
    
    return render(request, 'pages/projectmanager.html',{"ProjectData":ProjectData, "form":form,"employees":employee.objects.all()})


@login_required
def updateTask(request, f_id):
    obj = get_object_or_404(Task, taskID=f_id)
    
    if request.method=="POST":
        form = TaskForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('task')
    else:
        form = TaskForm(instance=obj)
        
    return render(request, 'pages/taskmanager.html',{"form":form,'task':obj})

@login_required
def updateProject(request, f_id):
    obj = project.objects.get(projectID=f_id)
    
    if request.method=="POST":
        form = ProjectForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('projMan')
    else:
        form = ProjectForm(instance=obj)
    
    return render(request, 'pages/projectmanager.html',{"form":form})

@login_required
def updateEmployee(request, f_id):
    obj = employee.objects.get(empID=f_id)
    
    if request.method=="POST":
        form = EmpForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('empMan')
    else:
        form = EmpForm(instance=obj)
    return render(request, 'pages/employeemanager.html',{"form":form})


@login_required
def deleteTask(request, f_id):
    obj = Task.objects.get(taskID=f_id)
    if request.method=="POST":
        obj.delete()
        return redirect('task')
    

@login_required
def deleteProject(request, f_id):
    obj = project.objects.get(projectID=f_id)
    if request.method=="POST":
        obj.delete()
        return redirect('projMan')
    

@login_required
def deleteEmployee(request, f_id):
    obj = employee.objects.get(empID=f_id)
    if request.method=="POST":
        obj.delete()
        return redirect('empMan')
    

def testFunc(request):
  
  employeeData = employee.objects.all()
  projectData = project.objects.all()
  assignmentData = assignments.objects.all()

  CompleteData = {
    "empData":employeeData,
    "projData":projectData,
    "asgnData":assignmentData
  }

  return render(request, "pages/fncTest.html",{"CompleteData" : CompleteData})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
        
def user_login(request):
    if request.method =='POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('/login')
