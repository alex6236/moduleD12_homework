from django.urls import path
from .views import RegisterView, LoginView, LogoutView

app_name = 'signup'
urlpatterns = [
    path('login_site/', LoginView.as_view(), name='login_site'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup_site/', RegisterView.as_view(), name='signup_site'),
]
