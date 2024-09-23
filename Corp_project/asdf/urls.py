from django.urls import path
from . import views



urlpatterns = [
    path('', views.Main_Page, name = '메인 페이지'),
    
]
