from faker import Faker
fake=Faker()
import random

from .models  import *
from .models import Student, Subject, SubjectMarks
from django.db.models import Sum

def create_subject_marks(n):
    try:
        students = Student.objects.all()
        subjects = Subject.objects.all()

        for student in students:
            for subject in subjects:
                subject_mark, created = SubjectMarks.objects.get_or_create(
                    student=student,
                    subject=subject,
                    defaults={'marks': random.randint(0, 100)}
                )
                if not created:
                    # Update the marks for an existing record if needed
                    subject_mark.marks = random.randint(0, 100)
                    subject_mark.save()
    except Exception as e:
        print(e)

def seed_db(n=10)->None:
    try:
        for _ in range(n):
            departments_objs=Department.objects.all()
            random_index=random.randint(0,len(departments_objs)-1)
            student_id=f'STU-0{random.randint(100,999)}'
            department=departments_objs[random_index]
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(20,30)
            student_address=fake.address()
            student_id_obj=StudentID.objects.create(student_id=student_id)

            student_obj=Student.objects.create(
                department= department,
                student_id= student_id_obj,
                student_email=student_email,
                student_name= student_name,
                student_age= student_age,
                student_address= student_address,          
            )
    except Exception as e:
        print(e)
       

def generate_report_card():
    curent_rank=-1
   
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-student_age')
    i=1
     
    for rank in ranks:
       ReportCard.objects.create(
            student=rank,
             student_rank=i
       )
       i=i+1