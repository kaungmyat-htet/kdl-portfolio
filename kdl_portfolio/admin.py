from django.contrib import admin
from .models import StudentCareerInfo, Project

class StudentCareerInfoAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(StudentCareerInfo, StudentCareerInfoAdmin)
admin.site.register(Project, ProjectAdmin)
