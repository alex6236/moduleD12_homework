from django.urls import path
from .views import AccountsView, upgrade_me #, SubscribeView, add_subscriber #subscribe_to_category #

app_name = 'users'
urlpatterns = [
    path('profile/', AccountsView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
   
]

