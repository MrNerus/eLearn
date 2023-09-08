from django.urls import path
from . import views as teacherView

urlpatterns = [
    path("", teacherView.index),
    path("index/", teacherView.index),
    path("login/", teacherView.login),
    path("editSubject/", teacherView.editSubject),

]