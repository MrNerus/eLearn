from django.urls import path
from . import views as adminView

urlpatterns = [
    path("", adminView.index),
    path("index/", adminView.index),
    path("login/", adminView.login),
    path("create/", adminView.create),
    path("create/grade", adminView.createGrade),
    path("create/section", adminView.createSection),
]