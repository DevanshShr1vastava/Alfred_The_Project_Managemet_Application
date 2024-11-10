from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class employee(models.Model):
    empID = models.IntegerField(primary_key=True)
    empName = models.CharField(max_length=255)
    empDesignation = models.CharField(max_length=255)
    def __str__(self):
        return self.empName


class project(models.Model):
    projectID = models.IntegerField(primary_key=True)
    projectName = models.CharField(max_length=255)
    projectProgress = models.IntegerField()
    projectDomain = models.CharField(max_length=255)
    projectLead = models.ForeignKey(employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.projectName

class assignments(models.Model):
    aID = models.IntegerField(primary_key=True)
    projID = models.ForeignKey(project,on_delete=models.CASCADE)
    eID = models.ForeignKey(employee,on_delete=models.CASCADE)

class Task(models.Model):
    taskID = models.AutoField(primary_key=True)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    taskName = models.CharField(max_length=255)
    isCompleted = models.BooleanField(default=False)
    assignedEmployee = models.ForeignKey(employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.taskName} - {'Completed' if self.isCompleted else 'Pending'} (Assigned to: {self.assignedEmployee.empName if self.assignedEmployee else 'Unassigned'})"
