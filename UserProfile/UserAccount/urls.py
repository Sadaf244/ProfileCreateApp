from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',UserSignupView,name='user-signup'),
    path('login/',LoginView,name='login'),
    path('updateprofile/',CreateProfileView,name='create-profile')
]