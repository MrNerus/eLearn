from django.contrib import admin
from .models import Admin, AdminInfo, Grade, Section, Subject, SectionSubject, Teacher, TeacherInfo, TeacherSubjects, Student, StudentInfo, StudentSubjects
# Register your models here.

admin.site.register(Admin)
admin.site.register(AdminInfo)

admin.site.register(Grade)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(SectionSubject)


admin.site.register(Teacher)
admin.site.register(TeacherInfo)
admin.site.register(TeacherSubjects)

admin.site.register(Student)
admin.site.register(StudentInfo)
admin.site.register(StudentSubjects)