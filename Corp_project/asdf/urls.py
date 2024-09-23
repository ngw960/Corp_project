from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.Main_Page, name = '메인 페이지'),

    path('signup/', views.Signup_Page, name = '회원가입 페이지'),

    path('signup_action/', views.Signup_Action, name = '회원 가입하기'),

    path('login/', views.Login_Page, name = '로그인 페이지'),

    path('login_action/', views.Login_Action, name = '로그인 하기'),

    path('logout/', views.Logout, name = '로그아웃'),

    
]
