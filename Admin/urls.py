
from django.urls import path
from . import views

urlpatterns = [

    path("login_page",views.login_here),
    path("admin_homepage", views.admin_homepage),
    path("register_college", views.register_college),
    path("view_colleges", views.view_colleges),
    path("view_full_info", views.view_full_info),
    path("view_profile", views.view_admin_profile),
    path("update_admin", views.update_admin),
    path("update_admin_profile", views.update_admin_profile),
    path("college_register_success", views.college_register_sucess),
    path("change_password", views.change_password),
    path("change_admin_password", views.change_admin_password),
    path("user_logout", views.user_logout),
    path("delete_college", views.delete_college),

    ]