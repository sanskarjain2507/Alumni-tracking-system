
from django.urls import path
from . import views

urlpatterns = [

    path("signup_page",views.signup_here),
    path("student_homepage",views.student_homepage),
    path("view_college_info",views.view_college_info),
    path("view_full_college_info",views.view_full_college_info),
    path("student_login_success",views.student_login_success),
    path("register_success",views.register_success),
    path("change_password",views.change_password),
    path("change_student_password",views.change_student_password),
    path("after_image_update",views.after_image_update),
    path("change_image",views.change_image),
    path("view_profile",views.view_student_profile),
    path("update_student",views.update_student),
    path('ajax/validate_email',views.validate_email),
    path('ajax/upvote',views.upvote_consensus),
    path('view_consensus',views.view_consensus),
    path('view_notices',views.view_notices),
    path('view_full_notice',views.view_full_notices),
    path("update_student_profile",views.update_student_profile),
    path("after_forgot_password",views.after_forget_password),
    path("forgot_pass_email",views.forgot_email_pass),
    path("verify_code",views.verify_code),
    path("reset_password",views.reset_password),



    ]