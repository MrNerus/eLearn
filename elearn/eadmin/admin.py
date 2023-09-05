from django.contrib import admin
from .models import Admin, AdminInfo, Grade, Section
# Register your models here.

admin.site.register(Admin)
admin.site.register(AdminInfo)
admin.site.register(Grade)
admin.site.register(Section)
