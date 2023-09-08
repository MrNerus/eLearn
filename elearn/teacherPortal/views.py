from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from eadmin.models import Teacher, TeacherSubjects, SectionSubject, StudentSubjects, StudentInfo, Subject
from datetime import datetime
from .factory import sessionHandeler
# Create your views here.

def index(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/teacherPortal/login")
    
    # Gets a information about this teacher
    thisTeacher = Teacher.objects.get(username=request.session["username"])
    teacherSubjects = list(TeacherSubjects.objects.filter(username=thisTeacher))

    classInfo = {}
    for i in teacherSubjects:
        i_class = (SectionSubject.objects.get(subject = i.subject).section).grade
        i_section = SectionSubject.objects.get(subject = i.subject).section
        allStudents = list(StudentSubjects.objects.filter(subject=SectionSubject.objects.get(subject = i.subject)))
        className = str(i_class)
        sectionName = str(i_section)
        if className in classInfo:
            if sectionName in classInfo[className]: 
                classInfo[className][sectionName][i.subject.name] = {
                    "id": i.subject.id,
                    "vidConf": i.subject.vidConference,
                    "classroomLink": i.subject.classroomLinks,
                    "jamLinks": i.subject.jamLinks,
                    "studentCount": len(allStudents),
                    "allStudents": [[j.username.username, StudentInfo.objects.get(username=j.username).name] for j in allStudents]                        
                }
            else:
                classInfo[className][sectionName] = {
                    i.subject.name: {
                            "id": i.subject.id,
                            "vidConf": i.subject.vidConference,
                            "classroomLink": i.subject.classroomLinks,
                            "jamLinks": i.subject.jamLinks,
                            "studentCount": len(allStudents),
                            "allStudents": [[j.username.username, StudentInfo.objects.get(username=j.username).name] for j in allStudents]
                        }
                    }
        else:
            classInfo[className] = {
                sectionName : {
                    i.subject.name : {
                        "id": i.subject.id,
                        "vidConf": i.subject.vidConference,
                        "classroomLink": i.subject.classroomLinks,
                        "jamLinks": i.subject.jamLinks,
                        "studentCount": len(allStudents),
                        "allStudents": [[j.username.username, StudentInfo.objects.get(username=j.username).name] for j in allStudents]
                    }
                }
            }
    return JsonResponse({"message":"Working Correctly", "classInfo": classInfo})

def editSubject(request):
    if not sessionHandeler.requestIsValid(request):
        return redirect("/teacherPortal/login")
    if request.method == "GET":
        sub = Subject.objects.get(id = request.GET.get('id'))
        json = {
            "id": sub.id,
            "name": sub.name,
            "vidConference": sub.vidConference,
            "jamLinks": sub.jamLinks
        }
        return JsonResponse(json)
    if request.method == "POST":
        sub = Subject.objects.get(id = request.POST.get('id'))
        sub.name = request.POST.get('name')
        sub.vidConference = request.POST.get('vidConference')
        sub.jamLinks = request.POST.get('jamLinks')
        sub.save()
        redirect("/teacherPortal/index")
    return JsonResponse({"message":"This Should not Happen"})
        

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pswd = request.POST.get('password')
        print(f"\'{pswd}\'")
        try:
            userInQuestion = Teacher.objects.get(username=uname)
            if check_password(pswd, userInQuestion.password):
                request.session["isLoggedIn"] = True
                request.session["username"] = userInQuestion.username
                request.session["name"] = userInQuestion.TeacherInfo.name
                request.session["accessLevel"] = "Teacher"
                request.session["loggedInTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session["activeTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # return JsonResponse({"message":"OK"})
                return redirect("/teacherPortal/index")
            return JsonResponse({"message":"Authorization Failed"})
        except Teacher.DoesNotExist:
            return JsonResponse({"message":"Invalid Username"})
    return render(request, 'teacherPortal/login.html')
