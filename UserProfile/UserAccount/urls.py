from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',UserSignupView),
    path('login/',LoginView),
    path('updateprofile/',CreateProfileView)
]