from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ImageField, FileInput



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)



class MyUserCreationForm(UserCreationForm):
    

    class Meta:

        model = User
        fields = ['email','username','password1','password2']

    
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['email','username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter Email','required': 'required'}
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter Username','required': 'required'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter Password','required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}

    def clean_username(self):
        description = self.cleaned_data.get('username')
        max_length = 12 # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'Username should be no more than {max_length} characters. (length = {len(description)})')
        return description


class ProfileUpdateForm(ModelForm):
    profile_pic = forms.FileField(required=False,widget=forms.FileInput) 
    class Meta:
        model = User
        fields = ["profile_pic",'email']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['email']:
            self.fields[fieldname].help_text = None

        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter Email','required': 'required'}
 

class MyPasswordChangeForm(PasswordChangeForm):
    

    class Meta:

        model = User
        fields = ['old_password','new_password1','new_password2']

    
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['old_password','new_password1','new_password2']:
            self.fields[fieldname].help_text = None

        self.fields['old_password'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter Old Password','required': 'required'}
        self.fields['new_password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Enter New Password','required': 'required'}
        self.fields['new_password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm New password','required': 'required'}

