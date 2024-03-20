from django.shortcuts import render,redirect
from .models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .forms import LoginForm,MyUserCreationForm,ProfileUpdateForm,MyPasswordChangeForm
from django.db import IntegrityError
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from chat.models import ChatRoom


# Create your views here.

class LoginView(LoginView,SuccessMessageMixin):

    template_name = 'account/login.html'
    form_class = LoginForm
    success_message = "Logged In successfully!"
    

    def get_success_url(self):
        messages.success(self.request,"Logged In Successfully")
        return reverse_lazy('index:index')
    
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)
    
    

class RegisterView(SuccessMessageMixin, generic.CreateView):
    model = User
    template_name = 'account/register.html'
    form_class = MyUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('account:login')
    success_message = "Account created successfully!"

    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.warning(self.request, 'username already exists!')
            return redirect('account:register')
    


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = 'account/settings.html'
    model = User
    form_class = ProfileUpdateForm
    success_message = 'Profile Picture Updated'

    def get_success_url(self):
        return reverse('account:edit-profile', kwargs={'slug': self.object.slug})

    def dispatch(self, request, slug, *args, **kwargs):
        if request.user.slug != slug:
            return redirect('account:edit-profile', slug=request.user.slug)
        return super().dispatch(request, slug=slug, *args, **kwargs)

    def form_valid(self, form):
        profile_picture = form.cleaned_data.get('profile_pic')
        if profile_picture:
            self.object.profile_picture = profile_picture
        return super().form_valid(form)
    

class PasswordChangeView( SuccessMessageMixin,PasswordChangeView):

    form_class = MyPasswordChangeForm
    template_name = 'account/password_change.html'
    
    success_message = "Password Changed Succesfully Please Log In Again"
    success_url = reverse_lazy('account:logout')



class DeleteAccountView(LoginRequiredMixin,SuccessMessageMixin,generic.DeleteView):


    model =User

    def get_success_url(self):
        return reverse_lazy('index:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        chatrooms = ChatRoom.objects.filter(members = request.user)

        for chatroom in chatrooms:
            chatroom.delete()
            
        self.object.delete()
        messages.success(request, f"Your account has been deleted successfully. However, you can still browse our website even without an account")
        return HttpResponseRedirect(self.get_success_url())


    





 