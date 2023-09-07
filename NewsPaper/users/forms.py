# from django import forms
# # from django.contrib.auth.models import User
# from users.models import Subscriber
 
# class SubscriberForm(forms.Form):
#     class Meta:
#         model = Subscriber
#         fields = ('user', 'email', 'category')

   

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Пользователь с таким именем уже существует")
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Пользователь с таким email уже существует")
    #     return super().clean()
