from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group


class RegisterForm(UserCreationForm):
    username = forms.CharField(label = "Имя", 
                widget=forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Имя пользователя',
                'class': 'form-control me-2',
                }))
    
    email = forms.CharField(label = "Email", 
                widget=forms.EmailInput(attrs={
                'type': 'email',
                'placeholder': 'name@example.com',
                'class': 'form-control me-2',
                }))
    
    first_name = forms.CharField(label = "Имя", 
                widget=forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Имя',
                'class': 'form-control me-2',
                }), required=False)
    
    last_name = forms.CharField(label = "Фамилия", 
                widget=forms.TextInput(attrs={
                'type': 'text',
                'placeholder': 'Фамилия',
                'class': 'form-control me-2',
                }), required=False)
    
    password1 = forms.CharField(max_length=16, 
                widget=forms.PasswordInput(attrs={
                'class': 'form-control me-2'}), label='Пароль')
    
    password2 = forms.CharField(max_length=16, 
                widget=forms.PasswordInput(attrs={
                'class': 'form-control me-2'}), label='Повторить пароль')
  
    class Meta:
        model = User
        fields = (
            "username",
            'first_name',
            'last_name',
            "email",
            "password1",
            "password2",
            )
        # widgets = {
        #    'username': forms.TextInput(attrs={'class': 'form-control'}),
           
        #    'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     }
      
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()
    
    def save(self, request):
       user = super(RegisterForm, self).save(request)
       common_group = Group.objects.get_or_create(name='common')[0]
       common_group.user_set.add(user)
       return user
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'


    # class Meta:
    #     model = User
    #     fields = (
    #         "username",
    #         "password",
    #         )
    #     widgets = {
    #        'username': forms.EmailInput(attrs={'class': 'form-control'}),
    #        'password': forms.TextInput(attrs={'class': 'form-control'}),
    #         }
