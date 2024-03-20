from django import forms
from .models import Post,Comment,Reply


class CreateTextBasedPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','content']


        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', }),
  
            
        }

    def clean_title(self):
        description = self.cleaned_data.get('title')
        max_length = 130 # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'title should be no more than {max_length} characters. (length = {len(description)})')
        return description


class CreateImageBasedPostForm(forms.ModelForm):

    image = forms.FileField(required=True,widget=forms.FileInput(attrs={'accept': 'image/*'}))
    class Meta:
        model = Post
        fields = ['title','image']


        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', }),
  
      
        }

    def clean_title(self):
        description = self.cleaned_data.get('title')
        max_length = 130 # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'title should be no more than {max_length} characters. (length = {len(description)})')
        return description


class CreateVideoBasedPostForm(forms.ModelForm):

    video = forms.FileField(required=True,widget=forms.FileInput(attrs={'accept': 'video/*'}))
    class Meta:
        model = Post
        fields = ['title','video']


        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', }),
  
      
        }

    def clean_title(self):
        description = self.cleaned_data.get('title')
        max_length = 130 # Specify your desired maximum length here
        if len(description) > max_length:
            raise forms.ValidationError(f'title should be no more than {max_length} characters. (length = {len(description)})')
        return description


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']



class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply']


    
