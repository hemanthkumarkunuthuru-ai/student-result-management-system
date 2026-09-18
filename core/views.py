from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.db import IntegrityError
from django.contrib import messages

def home(request):
    return render(request,"home.html")

def registerPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            User.objects.create_user(
                username=email,
                email=email,
                password=password1
            )
            messages.success(request, "Account created successfully. Please login 😊")
            return redirect("login")

    return render(request, "register.html")


def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            messages.success(request, "Login Successful 🎉")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Email or Password ❌")

    return render(request, "login.html")



def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request,"dashboard.html",{
        "students":Student.objects.count(),
        "subjects":Subject.objects.count(),
        "marks":Marks.objects.count()
    })

@login_required
def students(request):
    return render(request,"students.html",{"students":Student.objects.all().order_by('roll')})

@login_required
def addStudent(request):
    if request.method=="POST":
        Student.objects.create(
            roll=request.POST['roll'],
            name=request.POST['name'],
            course=request.POST['course'],
            semester=request.POST['semester'],
        )
        return redirect("students")
    return render(request,"add_student.html")

@login_required
def deleteStudent(request, roll):
    Student.objects.filter(roll=roll).delete()
    return redirect("students")


@login_required
def addMarks(request):
    students = Student.objects.all().order_by("roll")   # ordered by roll number
    subjects = Subject.objects.all()

    if request.method == "POST":
        student = Student.objects.get(id=request.POST["student"])
        subject = Subject.objects.get(id=request.POST["subject"])
        marks = request.POST["marks"]

        try:
            Marks.objects.create(
                student=student,
                subject=subject,
                marks=marks
            )
            messages.success(request, "Marks Saved Successfully ✔")

        except IntegrityError:
            messages.error(
                request,
                "⚠ This subject is already added for this student!"
            )

        return redirect("add_marks")

    return render(request, "add_marks.html",
                  {"students": students, "subjects": subjects})


@login_required
def searchStudent(request):
    student = None
    marks = None
    total = 0
    percentage = 0
    message = None

    if request.GET.get("roll"):
        student = Student.objects.filter(roll=request.GET["roll"]).first()

        if student:
            marks = Marks.objects.filter(student=student)
            total = sum(m.marks for m in marks)
            max_total = sum(m.subject.max_marks for m in marks)
            percentage = round((total/max_total)*100, 2) if max_total else 0
        else:
            message = "❌ No student found with this Roll Number."

    return render(request, "search.html", {
        "student": student,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "message": message
    })



