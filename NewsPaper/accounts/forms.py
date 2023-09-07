# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import LoginForm, SignupForm

class MailRegisterForm(SignupForm):
    
    first_name = forms.CharField(label = "Имя", 
                widget=forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Имя',
                'class': 'form-control',
                }), required=False)
    
    last_name = forms.CharField(label = "Фамилия", 
                widget=forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Фамилия',
                'class': 'form-control',
                }), required=False)
    
    def __init__(self, *args, **kwargs):
        super(MailRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label = "Имя пользователя", 
                widget=forms.TextInput(attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control',
                }),)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторить пароль'})
        self.fields['email'].label = '*Email'
        self.fields['password1'].label = '*Пароль'
        self.fields['password2'].label = '*Повторить пароль'

    def save(self, request):
       user = super(MailRegisterForm, self).save(request)
       common_group = Group.objects.get_or_create(name='common')[0]
       common_group.user_set.add(user) # type: ignore
       return user
      
    class Meta:
        model = User
        field_order = (
            "username",
            'first_name',
            'last_name',
            "email",
            "password1",
            "password2",
            )
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()
    
class MailLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MailLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'type': 'email'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['login'].label = 'Email'
        self.fields['password'].label = 'Пароль'

class PasswordChangeForm(SignupForm):

    class Meta:
        model = User
        field_order = (
            'oldpassword',
            "password1",
            "password2",
            )
        
        
    # def __init__(self, *args, **kwargs):
    #     super(PasswordChangeForm, self).__init__(*args, **kwargs)
    #     self.fields['oldpassword'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'oldpassword', 'placeholder': 'Текщий пароль'})
    #     self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password1', 'placeholder': 'Новый пароль'})
    #     self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password2', 'placeholder': 'Новый пароль(еще раз)'})
    #     self.fields['oldpassword'].label = '*Текщий пароль'
    #     self.fields['password1'].label = '*Новый пароль'
    #     self.fields['password2'].label = '*Новый пароль(еще раз)'