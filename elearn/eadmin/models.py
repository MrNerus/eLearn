from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class AdminInfo(models.Model):
    accessLevel = (
        ("SuperUser", "SuperUser"),
        # class teacher, coordinator, exam coordinator, etc can be added if needed
    )
    username = models.OneToOneField(Admin, related_name="AdminInfo", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    accessLevel = models.CharField(max_length=32, choices=accessLevel)

    def __str__(self):
        return f"{self.username.username}: {self.name} as {self.accessLevel}"
    
class Grade(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name}"
    
class Section(models.Model):
    grade = models.ForeignKey(Grade, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.grade.name}: {self.name}"
    
class Subject(models.Model):
    name = models.CharField(max_length=32)
    vidConference = models.CharField(max_length=128, null=True)
    classroomLinks = models.CharField(max_length=128, null=True)
    jamLinks = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"{self.name} "

class SectionSubject(models.Model):
    section = models.ForeignKey(Section, related_name="sectionSubject", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="sectionsubject", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.section.name}:::{self.subject.name}"


class Student(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class StudentInfo(models.Model):
    username = models.OneToOneField(Student, related_name="StudentInfo", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    rollNo = models.IntegerField()
    section = models.OneToOneField(Section, related_name="StudentInfo", null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.name} from {self.username}"

class StudentSubjects(models.Model):
    username = models.ForeignKey(Student, related_name="studentSubjects",  on_delete=models.CASCADE)
    subject = models.ForeignKey(SectionSubject, related_name="StudentSubjects", on_delete=models.CASCADE)


class Teacher(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
 
class TeacherInfo(models.Model):
    username = models.OneToOneField(Teacher, related_name="TeacherInfo", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    # subjects = models.ManyToManyField(Subject, related_name="TeacherInfo")
    def __str__(self):
        return f"{self.username.username}: {self.name}"
    
class TeacherSubjects(models.Model):
    username = models.ForeignKey(Teacher, related_name="teacherSubjects", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="teacherSubjects", null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.username.username} teaches {self.subject.name}"
# Rule
# Multiple Grades
# One Grade has mutiple Sections. But One section cannot be in multiple Grade
# One Section can have multipe subject. But one subject cannot be in multiple section.
# One Section can have multiple student. But one student cannot be in mutiple section.
# Many Students can read optional many subject of that section.
#

