from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils.text import slugify

class StudentManager(models.Manager):
     def get_queryset(self):
          return super().get_queryset().filter(is_deleted=False)

User=get_user_model()

# Create your models here.


class Department(models.Model):
        department=models.CharField(max_length=100)


        def __str__(self) -> str:
            return self.department
        
        class Meta:
            ordering=['department']

class StudentID(models.Model):
    student_id=models.CharField(max_length=100)

    def __str__(self)->str:
        return self.student_id
    
  
class Subject(models.Model):
    subject_name=models.CharField(max_length=100)

    def __str__(self)->str:
         return self.subject_name


class Student(models.Model):
    department=models.ForeignKey(Department, related_name="depart" ,on_delete=models.CASCADE)
    student_id=models.OneToOneField(StudentID,related_name="studentID",on_delete=models.CASCADE)
    student_name=models.CharField(max_length=100)
    student_email=models.EmailField(unique=True)
    student_age=models.IntegerField(default=18)
    student_address=models.TextField()
    is_deleted=models.BooleanField(default=False)


    objects=StudentManager()
    admin_objects=models.Manager()


    def __str__(self)->str:
        return self.student_name
    
    class Meta:
        ordering=['student_name']
        verbose_name="student" 

class SubjectMarks(models.Model):
        student=models.ForeignKey(Student,related_name="studentmarks",on_delete=models.CASCADE )
        subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
        marks=models.IntegerField()


        def __str__(self)->str:
             return f'{self.student.student_name} {self.subject.subject_name}'
             
        class Meta:
             unique_together=['student','subject']

from datetime import datetime

def get_unique_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%B %d, %Y")
    return timestamp

class ReportCard(models.Model):
    student = models.ForeignKey(Student, related_name="studentreportcard", on_delete=models.CASCADE)
    student_rank = models.IntegerField()
    date_of_report_card_generation = models.CharField(default=get_unique_timestamp, max_length=15)  # Use max_length=15 for "April 20, 2023"

    class Meta:
        unique_together = ['student_rank', 'date_of_report_card_generation']