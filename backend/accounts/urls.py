from django.urls import path,include
from .views import * 
urlpatterns = [
    # Accounts
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('',UserView.as_view())
]
