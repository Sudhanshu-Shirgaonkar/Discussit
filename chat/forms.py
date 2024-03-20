from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'name':'message','rows':1 ,'cols':200, 'class':'form-control autosize form-control-lg', 'style': 'resize: none; max-height: 100px;'}),
        }