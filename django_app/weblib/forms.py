from django import forms
from .models import Article, Comment, Folder, Good, Tag
from django.contrib.auth.models import User

# 検索用フォーム
class FindForm(forms.Form):
    find = forms.CharField(label='', required=False, \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['find'].widget = forms.HiddenInput()
    """

# コメント用フォーム
class CommentForm(forms.Form):
    content = forms.CharField(label='',max_length=1000, \
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':6}))

# Folder作成フォーム
class CreateFolderForm(forms.Form):
    folder_name = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'class':'form-control'}))

# Tag作成フォーム
class CreateTagForm(forms.Form):
    content = forms.CharField(label='',max_length=50, \
        widget=forms.TextInput(attrs={'class':'form-control'}))

# Tag作成フォーム
class CreateTagArrowForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(CreateTagArrowForm, self).__init__(*args, **kwargs)
        self.fields['content'] = forms.ChoiceField(label='',
            choices=[('-','タグを外す')] + [(item.title, item.title) \
                for item in Tag.objects.filter(owner=user)],
                widget=forms.RadioSelect(),
        )

# 投稿フォーム
class PostForm(forms.Form):
    title = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    link = forms.URLField(required=False, max_length=1000, \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    keyword = forms.CharField(max_length=100, \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(max_length=1000, \
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':6}))
    public = forms.BooleanField(required=False, \
        widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['folder_id'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                for item in Folder.objects. \
                filter(owner=user)],
                widget=forms.Select(attrs={'class':'form-control'}),
        )
    
    