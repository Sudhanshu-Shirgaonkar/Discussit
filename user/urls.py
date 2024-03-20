
from django.urls import path
from .import views

urlpatterns = [

    path("<slug:slug>",views.UserView.as_view(),name='user'),
    path("<slug:slug>/follow/", views.follow, name="follow"),
    path("<slug:slug>/submitted-posts/", views.SubmittedPostView.as_view(), name="submitted-post"),
    path("<slug:slug>/my-groups/", views.MyGroupView.as_view(), name="my-groups"),
    path("<slug:slug>/group-member-in/", views.MemberInGroupView.as_view(), name="group-member-in"),
    path("<slug:slug>/following/", views.FollowingView.as_view(), name="following"),
    path("<slug:slug>/followers/", views.FollowerView.as_view(), name="followers"),

    
    

]
