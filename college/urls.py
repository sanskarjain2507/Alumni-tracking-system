
from django.urls import path
from . import views

urlpatterns = [

    path("college_homepage",views.college_homepage),
    path("change_image",views.change_image),
    path("after_image_update",views.after_image_update),
    path("view_colleges",views.view_colleges),
    path("view_profile",views.view_profile),
    path("view_full_college_info",views.view_college_info),
    path("update_college",views.update_college),
    path("change_password",views.change_password),
    path("view_alumini_requests",views.view_alumini_request),
    path("verify_alumni",views.verify_alumini),
    path("publish_consensus",views.publish_consensus),
    path("publish_notice",views.publish_notice),
    path("send_notice",views.send_notice),
    path("view_notices",views.view_notices),
    path("view_full_notice",views.view_full_notice),
    path("submit_consensus",views.submit_consensus),
    path("view_consensus",views.view_consensus),
    path("discard_alumni",views.discard_alumini),
    path("view_alumni_full_info",views.view_alumni_info),
    path("change_college_password",views.change_college_password),
    path("update_college_profile",views.update_college_profile),
    path("view_location",views.view_location),
    path("ajax/validate_college_id",views.validate_college_id),
    path("view_full_vote_info",views.view_consensus_info),
    path("delete_notice",views.delete_notice),
    path("delete_consensus",views.delete_consensus),
    path("view_alumnis",views.view_alumnis),
    path("group_chat",views.group_chat),
    path("view_full_alumni_info",views.full_alumni_info),
    path("alumni_search",views.alumni_search),


    ]