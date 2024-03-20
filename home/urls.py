
from django.urls import path
from .import views

urlpatterns = [

    path("",views.IndexView.as_view(),name='index'),
    path("groups",views.AllGroups.as_view(),name='groups'),
    path("blocked/<slug:slug>",views.BlockedGroupView.as_view(),name='blocked-group'),
    path("private/<slug:slug>",views.PrivateGroupView.as_view(),name='private-group'),
]
