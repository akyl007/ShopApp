from django import forms
from .models import Messenger, Chat


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messenger
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ваше сообщение...'}),
        }