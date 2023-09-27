from django.urls import path
from . import views

urlpatterns = [
    path('webcam_rec/', views.webcam_recognition_view, name='webcam_recognition_view'),
    path('recognition_log/', views.recognition_log_view, name='recognition_log_view'),
]
