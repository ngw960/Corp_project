from django.shortcuts import render, redirect                         # 렌더링, 리디렉션
from Team_3E.models import Users                                      # DB 모델
from .models import Character                                         # Character 모델 import 추가
from django.contrib.auth import login                                 # Django 내장 시스템 (사용자 세션 로그인)
from django.contrib.auth.decorators import login_required             # 로그인한 사용자만 접근 가능하도록 제한
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 암호화, 암호화된 비밀번호와 기본 비밀번호 크로스체크
from django.contrib import messages                                   # Django 내장 시스템 (성공, 오류 등 피드백 전달용)
from django.shortcuts import render, get_object_or_404


# 인덱스 페이지
def Home (request):
    return render(request, "main.html")

# 회원가입 페이지
def Register (request):
    return render(request, "register.html")

# 회원가입 액션 처리
def Register_Action (request):
    # 입력받은 값 정의
    var_user_id  = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')
    var_name     = request.POST.get('input_name')
    var_email    = request.POST.get('input_email')

    # 빈 필드가 없는지 검증
    if not (var_user_id and var_password and var_name and var_email):
        messages.error(request, '모든 필드를 입력해주세요.')
        return redirect('회원가입')

    # 아이디 중복확인
    if Users.objects.filter(user_id=var_user_id).exists():
        messages.error(request, '이미 존재하는 아이디입니다.')
        return redirect('회원가입')

    # 이메일 중복확인
    if Users.objects.filter(email=var_email).exists():
        messages.error(request, '이미 존재하는 이메일입니다.')
        return redirect('회원가입')

    # 비밀번호 암호화 후 저장
    #encrypted_password = make_password(var_password)
    Users.objects.create(
        user_id  = var_user_id,
        password = var_password,
        name     = var_name,
        email    = var_email
    )

    # 회원가입 완료 후 로그인 페이지로 이동
    messages.success(request, '회원가입이 완료되었습니다. 로그인 해주세요.')
    return render(request, "user_login.html")

# 로그인 페이지
def Login (request):
    return render(request, "user_login.html")

# 로그인 액션 처리
def Login_Action(request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')

    # 빈 필드가 없는지 검증
    if not (var_user_id and var_password):
        messages.error(request, '아이디와 비밀번호를 모두 입력해주세요.')
        return redirect('로그인')

    # 입력된 아이디로 유저 조회
    select_user = Users.objects.filter(user_id=var_user_id).first()

    if not select_user:
        messages.error(request, '존재하지 않는 아이디입니다.')
        return redirect('로그인')

    # 비밀번호가 일치하는지 확인
    # 비밀번호 확인 로직 수정
    if select_user.password != var_password:  # 비밀번호가 일치하지 않을 때
        messages.error(request, '비밀번호가 일치하지 않습니다.')
        return redirect('로그인')

    # 유저 로그인
    login(request, select_user)
    messages.success(request, f'{var_user_id}님, 환영합니다!')
    return redirect('홈페이지')  # 로그인 성공 시 홈페이지로 리디렉션

# 로그아웃 처리
def Logout (request):
    # 세션 초기화
    request.session.flush()
    messages.success(request, '로그아웃되었습니다.')
    return redirect('홈페이지')

# 마이페이지
@login_required
def Mypage (request):
    return render(request, 'user_mypage.html',)

# 회원정보 수정 처리
@login_required
def Mypage_info_edit (request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_name    = request.POST.get('input_name')
    var_email   = request.POST.get('input_email')

    # 빈 필드가 없는지 검증
    if not (var_user_id and var_name and var_email):
        messages.error(request, '모든 필드를 입력해주세요.')
        return redirect('마이페이지')

    # 아이디 중복 확인
    if Users.objects.filter(user_id=var_user_id).exists():
        messages.error(request, '이미 존재하는 아이디입니다.')
        return redirect('마이페이지')

    # 이메일 중복 확인
    if Users.objects.filter(email=var_email).exists():
        messages.error(request, '이미 존재하는 이메일입니다.')
        return redirect('마이페이지')

    # 유저 정보 수정
    try:
        user = Users.objects.get(id=request.user.id)
        user.user_id = var_user_id
        user.name    = var_name
        user.email   = var_email
        user.save()
        messages.success(request, '회원정보가 성공적으로 수정되었습니다.')
    except Users.DoesNotExist:
        messages.error(request, '유저를 찾을 수 없습니다.')
        return redirect('마이페이지')

    return render(request, 'user_mypage.html')

# 캐릭터 생성 페이지
@login_required
def Character_Create(request):
    if request.method == 'POST':
        character_name = request.POST.get('character_name')  # 사용자가 입력한 캐릭터 이름
        character_description = request.POST.get('character_type')  # 캐릭터 종류를 설명으로 저장

        # 캐릭터 생성
        new_character = Character.objects.create(
            name=character_name,
            description=character_description,  # 종류를 설명으로 저장
            user=request.user  # 현재 로그인한 유저와 연관
        )

        # 캐릭터 생성 완료 후 메인 화면으로 리디렉션
        messages.success(request, '캐릭터가 성공적으로 생성되었습니다.')
        return redirect('홈페이지')

    return render(request, 'character_create.html')  # GET 요청 시 캐릭터 생성 페이지 렌더링

# 캐릭터 목록 페이지
@login_required
def Character_main(request):
    characters = Character.objects.filter(user=request.user)  # 현재 로그인한 사용자의 캐릭터만 조회
    return render(request, 'character_main.html', {'characters': characters})

# 캐릭터 상세정보 페이지
def Character_detail(request):
    return render(request, 'character_detail.html')

# 게임 메인페이지
def Game_Main(request):
    return render(request, 'game_main.html')

def Game_Rangking(request):
    return render(request, 'game_rangking.html')

def Game_Invite(request):
    return render(request, 'game_invite.html')

def Game_Challenge(request):
    return render(request, 'game_challenge.html')

def Game_Shop(request):
    return render(request, 'game_shop.html')

# 전투 페이지 뷰 함수
def Game_battle(request, level):
    if 'player_hp' not in request.session:
        request.session['player_hp'] = 200
        request.session['opponent_hp'] = 211
        request.session['battle_logs'] = []
        request.session['turn_counter'] = 1

    player_hp = request.session['player_hp']
    opponent_hp = request.session['opponent_hp']
    battle_logs = request.session['battle_logs']
    turn_counter = request.session['turn_counter']

    if request.method == 'POST':
        attack_type = request.POST.get('attack_type')

        if attack_type == 'strong':
            player_damage = 50
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 강한 공격으로 {player_damage}의 피해를 입혔습니다!")
        else:
            player_damage = 20
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 약한 공격으로 {player_damage}의 피해를 입혔습니다!")

        opponent_hp -= player_damage
        if opponent_hp <= 0:
            opponent_hp = 0

        if opponent_hp > 0:
            opponent_damage = 30
            battle_logs.append(f"{turn_counter}번째 턴: 상대방이 강한 공격으로 {opponent_damage}의 피해를 입혔습니다!")
            player_hp -= opponent_damage
            if player_hp <= 0:
                player_hp = 0

        turn_counter += 1

        request.session['player_hp'] = player_hp
        request.session['opponent_hp'] = opponent_hp
        request.session['battle_logs'] = battle_logs
        request.session['turn_counter'] = turn_counter

    context = {
        'player_hp': player_hp,
        'opponent_hp': opponent_hp,
        'battle_logs': battle_logs,
        'level': level  # 이 부분도 추가
    }

    return render(request, 'battle_page.html', context)



# 레벨 선택 페이지 뷰 함수
def Game_Challenge(request):
    cleared_levels = [1]  # 1단계만 클리어한 상태
    max_level = max(cleared_levels)  # 클리어한 최대 레벨 계산
    next_level = max_level + 1  # 다음 도전할 레벨 계산
    context = {
        'cleared_levels': cleared_levels,
        'max_level': max_level,
        'next_level': next_level,
        'levels': reversed(range(1, 11))  # 1단계와 2단계만 표시 (테스트용)
    }

    return render(request, 'game_challenge.html', context)

# 전투 상태 초기화 뷰
def Game_battle_reset(request, level):
    # 전투 상태를 초기화
    request.session['player_hp'] = 200
    request.session['opponent_hp'] = 211
    request.session['battle_logs'] = []
    request.session['turn_counter'] = 1

    # 초기화 후 해당 레벨의 전투 페이지로 이동
    return redirect('battle_page', level=level)