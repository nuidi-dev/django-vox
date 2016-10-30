from django import forms
from .models import Topic, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'text', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'name': 'title', 'id': 'topic-title', 'class': 'form-control'}),
            'category': forms.Select(attrs={'id': 'topic-cat', 'class': 'form-control'}),

        }
