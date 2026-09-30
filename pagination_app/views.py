import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Student
from random import randint
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def create_student(req):
    students = []
    for i in range(1,101):
        student = Student(
            name = f'student {i}',
            age = randint(18,25),
            marks = randint(35,100)
        )
        students.append(student)
    Student.objects.bulk_create(students)
    return JsonResponse({'status':'Students added successfully!'})

def display_students(req):
    students = Student.objects.all()
    paginator = Paginator(students,10)
    page_no = req.GET.get('page')
    stu_obj = paginator.get_page(page_no)
    return render(req,'display.html',{'students':stu_obj})

@method_decorator(csrf_exempt,name='dispatch')
class StudentView(View):
    def get(self,req):
        return HttpResponse('I am Get')

    def post(self,req):
        return HttpResponse('I am Post')

    def put(self,req):
        return HttpResponse('I am Put')

    def delete(self,req):
        return HttpResponse('I am Delete')

@method_decorator(csrf_exempt,name='dispatch')
class AddStudent(View):
    def post(self,req):
        json_data = json.loads(req.body)
        Student.objects.create(
            name = json_data.get('name'),
            age = json_data.get('age'),
            marks = json_data.get('marks')
        )
        return JsonResponse({'status':'Student Added..!'})

@method_decorator(csrf_exempt,name='dispatch')
class GetStudent(View):
    def get(self,req,id):
        stu_obj = Student.objects.get(id=id)
        res={
            'name':stu_obj.name,
            'age':stu_obj.age,
            'marks':stu_obj.marks
        }
        return JsonResponse({'student':res})

    def patch(self,req,id):
        json_data = json.loads(req.body)
        stu_obj = Student.objects.get(id=id)
        stu_obj.name = json_data.get('name')
        stu_obj.age = json_data.get('age')
        stu_obj.marks = json_data.get('marks')
        stu_obj.save()
        return JsonResponse({'status':'Student Updated..!'})

    def delete(self,req,id):
        stu_obj = Student.objects.get(id=id)
        stu_obj.delete()
        return JsonResponse({'status':'Student Deleted..!'})