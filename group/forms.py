from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'category', 'description', 'group_type']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', }),
            'category': forms.Select(attrs={'class':'form-select'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':30, 'class':'form-control','id':'summary' }),
            'group_type': forms.Select(attrs={'class':'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.islower():
            raise forms.ValidationError('Group name should be in lowercase.')
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        max_length = 500  # Specify your desired maximum length here
        if len(description) > max_length: 
            raise forms.ValidationError(f'Description should be no more than {max_length} characters.  (length ={len(description)})')
        return description
    
    def clean_name_name(self):
        description = self.cleaned_data.get('name')
        max_length = 17 # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'Name should be no more than {max_length} characters.')
        return description



class EditGroupForm(forms.ModelForm):

    group_picture = forms.FileField(required=False,widget=forms.FileInput) 
    cover_picture = forms.FileField(required=False,widget=forms.FileInput) 

    class Meta:
        model = Group
        fields= [
            'category',
            'description', 'group_type',
            'group_picture','cover_picture',
            'allow_text_posts','allow_image_posts',
            'allow_video_posts',
            'approve_members','approve_post'
            ] 


        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', }),
            'category':forms.Select(attrs={'class':'form-select'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':30, 'class':'form-control','id':'summary'}),
            'group_type':forms.Select(attrs={'class':'form-select'}),
        
            

        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        max_length = 500  # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'Description should be no more than {max_length} characters. (length ={len(description)})')
        return description



class AdminModGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['moderator','admins']







