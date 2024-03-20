from django.urls import path,include
from django.contrib.auth.views import LogoutView

from .import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name= 'login'),
    path('register/',views.RegisterView.as_view(),name= 'register'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
    path('edit-profile/<slug:slug>/', views.EditProfileView.as_view(), name='edit-profile'),

    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('delete-account/<slug:slug>/', views.DeleteAccountView.as_view(), name='delete-account'),
 
    
]
