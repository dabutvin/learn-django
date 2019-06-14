from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
        max_length=4000,
        help_text='The maximum length is 4000 characters.')

    class Meta:
        model = Topic
        fields = ['subject', 'message']
