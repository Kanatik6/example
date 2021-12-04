from django.urls import path

from .views import LoginAPIView,RegistrationAPIView,LogoutAPIView

urlpatterns = [
    path('registration/',RegistrationAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    # * если прописываешь свои юрлы, то всегда нужно использовать .as_view(),они есть у всех-всех 
]