from django.urls import path
from .views import MailRegisterView, MailLoginView, PasswordChangeView #SocialAccountLoginViev   # LogoutView

app_name = 'accounts'
urlpatterns = [
    path('signup/', MailRegisterView.as_view(), name='signup'),
    path('login/', MailLoginView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
]
