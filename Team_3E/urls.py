from django.urls import path
from . import views

urlpatterns = [
    # 홈페이지
    path('',                  views.Home,             name='홈페이지'),
    # 회원
    path('register/',         views.Register,         name='회원가입'),
    path('register_action/',  views.Register_Action,  name='회원가입_액션'),
    path('login/',            views.Login,            name='로그인'),
    path('login_action/',     views.Login_Action,     name='로그인_액션'),
    path('logout/',           views.Logout,           name='로그아웃'),
    path('mypage/',           views.Mypage,           name='마이페이지'),
    path('mypage/info/edit/', views.Mypage_info_edit, name='회원정보수정'),
]
