from django.urls import path
from main.views import (
    show_main,
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_projects,
    create_project,
    delete_project,
    get_projects_json,
    toggle_star,
    
    ### ====== Tutorial 4 ====== ###
    register,
    login_user,
    logout_user,
    
    ### ===== Tugas 4 ====== ###
    toggle_star_experience,
    
    ### ====== Tutorial 5 ====== ###
    create_project_ajax,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    ### ====== Experience ======
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    
    ### ====== Projects ======
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    
    ### ====== Tutorial 4 ====== ###
    ### Logout dan Login
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    
    ### ====== Tugas 4 ====== ###
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),
    
    ### ====== Tutorial 5 ====== ###
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]