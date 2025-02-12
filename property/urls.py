from django.urls import path
from .views import (
    chat_with_author, create_index, delete_property_comment, delete_property_file, edit_property, property_comment,
    property_comment_reply,  property_detail, property_index, property_list, request_mobile, success_page, track_like, track_report,
    track_share, track_unlike, track_view, add_favourite, remove_favourite
)

urlpatterns = [
    path('property/<int:property_id>/edit/', edit_property, name='edit_property'),
    path('property/file/delete/<str:file_type>/<int:file_id>/', delete_property_file, name='delete_property_file'),


    path('property/<slug:property_slug>/', property_detail, name='property_detail'),
    

    path('properties/', property_list, name='property_list'),
    path('properties/<str:property_type>/', property_list, name='property_list'),
    path('properties/', property_list, name='all_properties'),

    # Like and Unlike URLs
    path('property/<int:property_id>/like/', track_like, name='property-like'),
    path('property/<int:property_id>/unlike/', track_unlike, name='property-unlike'),

    # Share and View URLs
    path('property/<int:property_id>/share/', track_share, name='property-share'),
    path('property/<int:property_id>/view/', track_view, name='property-view'),

    # Report URL
    path('property/<int:property_id>/report/', track_report, name='property-report'),

    # Comment-related URLs
    path('property/<int:property_id>/comment/', property_comment, name='property_comment'),
    path('property/<int:property_id>/comment/<int:parent_id>/reply/', property_comment_reply, name='property_comment_reply'),
    path('property/comment/<int:comment_id>/delete/', delete_property_comment, name='delete_property_comment'),

    # Favorite URLs
    path('property/<int:property_id>/favourite/add/', add_favourite, name='add_favourite'),
    path('property/<int:property_id>/favourite/remove/', remove_favourite, name='remove_favourite'),

    

     path('success/', success_page, name='success_page'),
     path('icreate/', create_index, name='create_index'),

     path('property/', property_index, name='property_index'),
     
    path("chat/<int:author_id>/", chat_with_author, name="chat_with_author"),
     
    path("request-mobile/", request_mobile, name="request_mobile"),
    
]
