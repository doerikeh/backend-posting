from django.urls import path
from .views import project_list, profiles, project_detail, profiles_detail

app_name = "profiles"

urlpatterns = [
    path("project/", project_list, name='project-list'),
    path("project/<slug>/", project_detail),
    path("profiles/<slug>/", profiles_detail, name="user-detail"),
    path("profiles/", profiles, name="profiles")
]