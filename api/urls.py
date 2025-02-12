# account/urls.py

from django.urls import path

from api import views



urlpatterns = [
    path('login/', views.login_view, name='api_login'),  # Login View (renders login page)
    path('logout/', views.logout_view, name='api_logout'),  # Add this line for logout
    path('create/', views.create_view, name='create'),  # Create View (renders create page)
    path('success/', views.success, name='success'),

    path('home/', views.home, name='api_home'),

    path('landcreate/', views.LandProperty_create, name='LandProperty_create'),
    path('residentialcreate/', views.ResidentialProperty_create, name='residentialproperty_create'),
    path('commercialcreate/', views.CommercialProperty_create, name='commercialproperty_create'),
    path('industrialcreate/', views.IndustrialProperty_create, name='industrialproperty_create'),

    path('properties/<int:pk>/', views.property_detail, name='property-detail'),
    
    path('api/properties/<int:pk>/', views.property_details_api, name='property-details-api'),
    
    path('api/properties/<int:property_id>/like/', views.TrackLikeView.as_view(), name='track-like'),
     path('api/properties/<int:property_id>/unlike/', views.TrackUnlikeView.as_view(), name='track-unlike'),
     path('property/<int:property_id>/favorite/', views.TrackFavoriteView.as_view(), name='property-favorite'),
    path('property/<int:property_id>/unfavorite/', views.TrackUnfavoriteView.as_view(), name='property-unfavorite'),
     path('api/properties/<int:property_id>/view/', views.TrackViewView.as_view(), name='track-view'),  # New URL pattern
    path('api/properties/<int:property_id>/action/<str:action_type>/', views.TrackActionView.as_view(), name='track-action'),
    path('api/properties/<int:property_id>/report/', views.TrackReportView.as_view(), name='track-report'),
    
    path('api/properties/<int:property_id>/comment/', views.TrackCommentView.as_view(), name='track-comment'),  # New URL pattern
    path('api/properties/<int:property_id>/comment/<int:parent_id>/reply/', views.TrackCommentReplyView.as_view(), name='track-comment-reply'),  # New URL pattern
    path('api/comments/<int:comment_id>/delete/', views.TrackDeleteCommentView.as_view(), name='track-delete-comment'),  


    path('get_location/', views.get_location, name='get_location'),
    path('get-coordinates/', views.get_coordinates, name='get_coordinates'),
    
]
