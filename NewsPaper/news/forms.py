from django import forms
from .models import *
# ==============================
from django.contrib.auth.models import User

class DateFilterForm(forms.Form):
    dataCreation__gt = forms.DateField(
            label='Дата создания', 
            widget=forms.TextInput(attrs={
            'type': 'date',
            'name': 'dataCreation',
            'value': '2023-06-05',
            'class': 'form-control me-2 shadow',
        }), required=False)

class TitleFilterForm(forms.Form):
    title__iregex = forms.CharField(
            label='Заголовок', 
            widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'title',
            'placeholder': 'Поиск по заголовку',
            'class': 'shadow form-control me-2',
        }), required=False)
    
class TtextFilterForm(forms.Form):
    text__iregex = forms.CharField(
            label='Содержание', 
            widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'text',
            'placeholder': 'Поиск по содержанию',
            'class': 'shadow form-control me-2',
        }), required=False)

class UsernameFilterForm(forms.Form):
    author__authorUser__username__iregex = forms.CharField(
            label='Автор', 
            widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'author',
            'placeholder': 'Поиск по имени автора',
            'class': 'form-control me-2',
        }), required=False)
    
class AddPostForm(forms.ModelForm):
    title = forms.CharField(max_length=124, 
            label='Заголовок',
            widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'title',
            'placeholder': 'Введите название статьи',
            'class': 'form-control me-2',
        }))
    text = forms.CharField(
            label='Содержание статьи',
            widget=forms.Textarea(attrs={
            'cols': 60, 'rows': 10,
            'type': 'text',
            'name': 'text',
            'placeholder': 'Текст статьи',
            'class': 'form-control me-2',
        }))
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
            label='Категория',
            widget=forms.Select(attrs={
            # 'type': 'text',
            'name': 'category',
            # 'placeholder': 'Категория на выбрана',
            'class': 'form-control me-2',
        }))

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите категорию"
        self.author_id = kwargs.pop('author_id', None)  # получаем author_id из kwargs
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'category', 'text']
        
        
class SubscriberForm(forms.Form):
    user = forms.CharField(max_length=100)
    email = forms.EmailField()
    category = forms.CharField(max_length=100)
    
    # class Meta:
    #     # model = Subscriber
    #     fields = ('user', 'email', 'category')


       