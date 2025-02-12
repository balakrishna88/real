from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # Room URLs
    path('room/', views.room_list, name='room_list'),  # Room list
    path('room/create/', views.create_room, name='create_room'),  # Create room
    path('room/<int:id>/', views.room_detail, name='room_detail'),

    #group
    path('group/', views.group_list, name='group_list'),
    path('group/create/', views.create_group, name='create_group'),
    
    path('group/settings/', views.group_settings, name='group_settings'),
    path('group/<str:group_name>/', views.group_detail, name='group_detail'),
    path('group/manage/<int:group_id>/', views.manage_group, name='manage_group'),

    path('group/<int:group_id>/request-to-join/', views.request_to_join_group, name='request_to_join_group'),
    path('join-request/<int:request_id>/approve/', views.approve_join_request, name='approve_join_request'),
    path('join-request/<int:request_id>/reject/', views.reject_join_request, name='reject_join_request'),

    path('group/<int:group_id>/update_stats/<str:stat_type>/', views.update_group_stats, name='update_group_stats'),

    path("group/<int:group_id>/report/", views.report_group, name="report_group"),
    path('group/<str:group_name>/join/', views.group_join, name='group_join'),
    
    
    
]
