from django.urls import path

## define here path
from .views import *
urlpatterns = [
    path('',signup,name='signup'),
    path('login/',loginUser),
    path('logout/',signout)
]
