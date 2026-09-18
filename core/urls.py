from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('students/', views.students, name="students"),
    path('add-student/', views.addStudent, name="add_student"),
    path('delete/<str:roll>/', views.deleteStudent, name="delete"),

    path('add-marks/', views.addMarks, name="add_marks"),
    path('search/', views.searchStudent, name="search"),
]
