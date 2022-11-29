from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    text = forms.CharField(required=True)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Разместить пост без группы',
        required=False
    )

    class Meta:
        model = Post
        fields = ('text', 'group',)
