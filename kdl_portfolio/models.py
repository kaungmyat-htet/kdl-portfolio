"""
Database models for kdl_portfolio.
"""
import logging

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.core.validators import RegexValidator
# from model_utils.models import TimeStampedModel

log = logging.getLogger(__name__)

User = get_user_model()
    
class StudentCareerInfoManager(models.Manager):
    def submit_student_career_info(self, student, student_career_obj):
        try:
            # student = Student.objects.get(id=student_career_obj["id"])
            obj, is_created = self.get_or_create(
                student=student,
                profession=student_career_obj["profession"],
                highest_level_degree = student_career_obj["highest_level_degree"],
                institution = student_career_obj["institution"],
                skills = student_career_obj["skills"]
            )
        except IntegrityError:
            log.error(
                "An error raised while trying to create student career info for %s", student_career_obj["id"]
            )
            is_created = False
        
        return is_created
    
class ProjectManager(models.Manager):
    def submit_project(self, user, project_obj):
        try:
            obj, is_created = self.get_or_create(
                student_id=user,
                description = project_obj["description"],
                title = project_obj["title"],
                project_url = project_obj["project_url"],
                role = project_obj["role"],
                start_date = project_obj["start_date"],
                end_date = project_obj["end_date"]
            )
        except IntegrityError:
            log.error(
                "An error occured while trying to create a new project."
            )
            is_created = False
        return is_created
    

class StudentCareerInfo(models.Model):
    """
    Model for Student Career Info
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    student = models.OneToOneField(
        User,
        on_delete= models.CASCADE,
        primary_key=True
    )
    profession = models.CharField(max_length=50, null=False)
    highest_level_degree = models.TextField(null=False)
    institution = models.CharField(max_length=140, null=False)
    skills = models.JSONField(default=dict)

    objects = StudentCareerInfoManager()

    def __str__(self) -> str:
        return '{}'.format(self.student)

class Project(models.Model):
    """
    Create Projects that students have done
    """
    title = models.CharField(max_length=120, null=False)
    description = models.TextField()
    student_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    project_url = models.URLField()
    role = models.CharField(max_length=40)
    start_date = models.DateField()
    end_date = models.DateField()

    objects = ProjectManager()

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '{}'.format(self.title)
