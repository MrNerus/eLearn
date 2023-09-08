from django.urls import path
from . import views as adminView

urlpatterns = [
    path("", adminView.index),
    path("index/", adminView.index),
    path("login/", adminView.login),
    path("create/", adminView.create),
    path("create/grade", adminView.createGrade),
    path("create/section", adminView.createSection),
    path("create/subject", adminView.createSubject),
    path("create/students", adminView.addStudents),
    path("create/teachers", adminView.addTeachers),
    path("create/assignSubject", adminView.assignSubject),
    path("create/assignStudentSubject", adminView.assignStudentSubject),
]