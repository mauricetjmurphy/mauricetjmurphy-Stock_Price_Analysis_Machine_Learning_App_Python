from django.urls import path
from backend import views

urlpatterns = [

    path('', views.getPredictions, name="predictions"),

    ]