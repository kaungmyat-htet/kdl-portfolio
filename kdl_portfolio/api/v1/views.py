import os
import logging
import requests
import json

from django.conf import settings
from rest_framework.decorators import api_view
from openedx.core.lib.api.view_utils import view_auth_classes
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from rest_framework import status, permissions
from rest_framework.permissions import BasePermission
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser

from kdl_portfolio.models import (
    Project,
    StudentCareerInfo
)

from django.contrib.auth import get_user_model

# from dotenv import load_env

# load_env()

# TOKEN = os.getenv("TOKEN")

log = logging.getLogger(__name__)


User = get_user_model()

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class isAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or request.user and request.user.is_superuser):
            return True
        return False
    
def serialize_project(project_obj):
    serialized_project = {}
    serialized_project["title"] = project_obj.title
    serialized_project["description"] = project_obj.description
    serialized_project["project_url"] = project_obj.project_url
    serialized_project["role"] = project_obj.role
    serialized_project["start_date"] = project_obj.start_date
    serialized_project["end_date"] = project_obj.end_date

    return serialized_project


def get_student_info(username):
    # log.info(settings.LMS_BASE_URL)
    url = f'{settings.LMS_BASE_URL}api/user/v1/accounts/{username}'
    # log.info(url)
    headers = {
        "Authorization": f"Bearer {settings.SECRET_TOKEN}"
    }
    res = requests.get(url, headers=headers)

    user_info = json.loads(res.text)
    return user_info

def get_student_certificates(username):
    url = f'{settings.LMS_BASE_URL}api/certificates/v0/certificates/{username}'
    headers = {
        "Authorization": f"Bearer {settings.SECRET_TOKEN}"
    }
    res = requests.get(url, headers=headers)

    certificates = json.loads(res.text)
    return certificates

@api_view(["GET"])
def get_student_profile(request, username):
    if request.method == 'GET':
        response = {}
        try:
            personal_info = {}
            student = User.objects.get(username=username)
            try:
                student_info = StudentCareerInfo.objects.get(student=student)
                personal_info["profession"] = student_info.profession
                personal_info["highest_level_degree"] = student_info.highest_level_degree
                personal_info["institution"] = student_info.institution
                personal_info["skills"] = student_info.skills
            except StudentCareerInfo.DoesNotExist:
                log.info("Student info does not exist.")
            user_info = get_student_info(username)
            if user_info["account_privacy"] != 'all_users':
                return Response({"detail": "User profile is private."}, status=status.HTTP_400_BAD_REQUEST)
            certificates = get_student_certificates(username)
            personal_info["name"] = user_info["name"]
            personal_info["username"] = user_info["username"]
            personal_info["email"] = user_info["email"]
            personal_info["profile_image"] = user_info["profile_image"]
            personal_info["bio"] = user_info["bio"]
            personal_info["level_of_education"] = user_info["level_of_education"]
            personal_info["social_links"] = user_info["social_links"]
            response["certificates"] = certificates
            response["personal_info"] = personal_info
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User Info does not found."}, status=status.HTTP_400_BAD_REQUEST)
    
@view_auth_classes(is_authenticated=True)
class StudentCareerInfoAPIView(APIView):
    """
    Create a student career info
    """
    REQUIRED_KEYS = ['profession', 'highest_level_degree', 'institution', 'skills']

    def _validate(self, career_info_obj):
        for key in self.REQUIRED_KEYS:
            if key not in career_info_obj:
                raise ValidationError(_("Key '{key}' not found.").format(key=key))

        return career_info_obj
    
    def get(self, request):
        if request.user:
            response = {}
            try:
                student = User.objects.get(username=request.user)
                try:
                    student_info = StudentCareerInfo.objects.get(student=student)
                    response["profession"] = student_info.profession
                    response["highest_level_degree"] = student_info.highest_level_degree
                    response["institution"] = student_info.institution
                    response["skills"] = student_info.skills
                except StudentCareerInfo.DoesNotExist:
                    log.info("Student info does not exist.")

                user_info = get_student_info(request.user)
                
                response["name"] = user_info["name"]
                response["username"] = user_info["username"]
                response["email"] = user_info["email"]
                response["profile_image"] = user_info["profile_image"]
                response["bio"] = user_info["bio"]
                response["level_of_education"] = user_info["level_of_education"]
                response["social_links"] = user_info["social_links"]
                response["certificates"] = user_info["course_certificates"]
                return Response(response, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User Info does not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Please login first to check your info."}, status=status.HTTP_400_BAD_REQUEST)
            
    
    def post(self, request):
        career_info_object = request.data
        try:
            if request.user:
                username = request.user
                try:
                    student = User.objects.get(username = username)
                except User.DoesNotExist:
                    return Response({"error": "The user does not exists"})
                career_info_object = self._validate(career_info_object)
                # log.info(career_info_object)
                StudentCareerInfo.objects.submit_student_career_info(student, career_info_object)
            else:
                return Response({"detail": "Please make sure you logged into our system."})
        except ValidationError as exc:
            return Response({
                "detail": _(' ').join(str(msg) for msg in exc.messages),
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Student career path info created successfully."}, status=status.HTTP_201_CREATED)
    
@view_auth_classes(is_authenticated=True)
class ProjectAPIView(APIView):
    """
    Projects API View
    """
    REQUIRED_KEYS = ['description', 'title', 'project_url', 'role', 'start_date', 'end_date']
    def _validate(self, project_obj):
        for key in self.REQUIRED_KEYS:
            if key not in project_obj:
                raise ValidationError(_("Key '{key}' not found.").format(key=key))
            
        return project_obj

    def get(self, request):
        if request.user:
            projects_list = []
            projects = Project.objects.filter(student_id=request.user)
            for project in projects:
                project_obj = serialize_project(project)
                projects_list.append(project_obj)

            return Response({"projects": projects_list}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Please login first."}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        project_object = request.data
        username = request.user
        if username:
            try:
                project = self._validate(project_object)
                try:
                    student = User.objects.get(username = username)
                except User.DoesNotExist:
                    return Response({"detail": "The user does not exists"})
                Project.objects.submit_project(student, project)
                return Response({"detail": "Project created successfully."}, status=status.HTTP_200_OK)
            except ValidationError as exc:
                return Response({
                    "detail": _(' ').join(str(msg) for msg in exc.messages),
                }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["GET"])
def get_student_projects(request, username):
    if request.method == 'GET':
        response = {}
        try:
            projects_list = []
            try:
                student = User.objects.get(username = username)
            except User.DoesNotExist:
                return Response({"detail": "The user {} does not exists".format(username)}, status=status.HTTP_400_BAD_REQUEST)
            projects = Project.objects.filter(student_id=student)
            for project in projects:
                project_obj = serialize_project(project)
                projects_list.append(project_obj)
            response["projects"] = projects_list
            return Response(response, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"detail": "The project does not exists"}, status=status.HTTP_400_BAD_REQUEST)
