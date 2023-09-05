from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .models import Admin, Grade, Section
from datetime import datetime
import json
from .factory import sessionHandeler
# Create your views here.

def index(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/eadmin/login")
    return render(request, 'eadmin/index.html')

# alows admin to create new Grade, add teacher etc.
def create(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/eadmin/login")
    tmp = Grade.objects.all()
    allGrade = {f"{i.id}" :f"{i.name}" for i in tmp}
    allInfo = {"grades": allGrade}
    return render(request, 'eadmin/create.html', context=allInfo)
    
def createGrade(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/eadmin/login")
    failedList = []
    if request.method == 'POST':
        for i in request.POST.keys():
            try: 
                if "grade" in i: Grade.objects.create(name=request.POST[i]).save()
            except:
                failedList.append(request.POST[i])
        if bool(failedList):
            return JsonResponse({"message":f"Error occured on adding {str(failedList)}"})
    return render(request, 'eadmin/create.html')
def createSection(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/eadmin/login")
    failedList = []
    if request.method == 'POST':
        data = json.loads(request.body)
        for i in data:
            for j in data[i]:
                try:
                    Section.objects.create(grade=Grade.objects.get(id = i), name=j).save()
                except: 
                    failedList.append((Grade.objects.get(id = i).name,j))
        if bool(failedList):
            return JsonResponse({"message":f"Unable to add {str(failedList)}"})

        return JsonResponse({"message": "ok"})

    # if request.method == 'POST':
    #     for i in request.POST.keys():
    #         try: 
    #             if "section" in i: Grade.objects.create(name=request.POST[i]).save()
    #         except:
    #             failedList.append(request.POST[i])
    #     if bool(failedList):
    #         return JsonResponse({"message":f"Error occured on adding {str(failedList)}"})
    return render(request, 'eadmin/create.html')


def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            userInQuestion = Admin.objects.get(username=uname)
            if check_password(pswd, userInQuestion.password) and userInQuestion.AdminInfo.accessLevel == "SuperUser":
                request.session["isLoggedIn"] = True
                request.session["username"] = userInQuestion.username
                request.session["name"] = userInQuestion.AdminInfo.name
                request.session["accessLevel"] = userInQuestion.AdminInfo.accessLevel
                request.session["loggedInTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session["activeTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # return JsonResponse({"message":"OK"})
                return redirect("/eadmin/index")
            return JsonResponse({"message":"Authorization Failed"})
        except Admin.DoesNotExist:
            return JsonResponse({"message":"Invalid Username"})
    return render(request, 'eadmin/login.html')
