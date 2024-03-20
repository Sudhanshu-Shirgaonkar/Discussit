
from django.urls import path
from .import views

urlpatterns = [

    path("<slug:slug>",views.GroupView.as_view(),name='group'),
  
    path("create/create_group",views.CreateGroupView.as_view(),name='create-group'),

    path("<slug:slug>/update_group",views.EditGroupView.as_view(),name='update-group'),
    path("join/<slug:slug>", views.group_join, name="group_join"),
    path("leave/<slug:slug>", views.group_leave, name="group_leave"),
    path('<slug:slug>/admin-mod/', views.AdminModView.as_view(), name='admin_mod'),
    path('<slug:slug>/approve-user/', views.ApproveMemberView.as_view(), name='approve-user'),
    path('<slug:slug>/block-remove/', views.BlockedUsersView.as_view(), name='block-remove'),
    path('<slug:slug>/approve-posts/', views.ApprovePostView.as_view(), name='approve-post'),
    path('<slug:slug>/delete-group', views.DeleteGroupView.as_view(), name='delete-group'),

    
  

]
