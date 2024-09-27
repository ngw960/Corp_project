from django.urls import path
from . import views

urlpatterns = [
    
    ## Basic

    # 홈페이지
    path('',                                  views.Home,                        name='홈페이지'),
    
    # 회원
    path('register/',                         views.Register,                    name='회원가입'),
    path('register_action/',                  views.Register_Action,             name='회원가입_액션'),
    path('login/',                            views.Login,                       name='로그인'),
    path('login_action/',                     views.Login_Action,                name='로그인_액션'),
    path('logout/',                           views.Logout,                      name='로그아웃'),
    path('mypage/',                           views.Mypage,                      name='마이페이지'),
    path('mypage/info/edit/',                 views.Mypage_info_edit,            name='회원정보수정'),
    
    ## Game

    # 캐릭터
    path('character/',                       views.Character_main,               name='캐릭터_목록'),
    path('character/<int:user_id>',          views.Character_detail,             name='캐릭터_상세정보'),
    path('character/create/',                views.Character_Create,             name='캐릭터_생성'),

    # 게임
    path('game_main/',                       views.Game_Main,                    name='게임_메인'),
    path('game_invite/',                     views.Game_Invite,                  name='방문'),
    path('game_challenge/',                  views.Game_Challenge,               name='도전'),
    path('game_battle/<int:level>/',         views.Game_battle,                  name='배틀'),
    path('game_battle_reset/<int:level>/',   views.Game_battle_reset,            name='배틀_초기화'),
    path('game_rangking/',                   views.Game_Rangking,                name='랭킹'),
    path('game_shop/',                       views.Game_Shop,                    name='상점'),

]
