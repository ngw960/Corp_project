from django.shortcuts import render, redirect                         # 렌더링, 리디렉션
from Team_3E.models import Users                                      # DB 모델
from .models import Character                                         # Character 모델 import 추가
from django.contrib.auth import login                                 # Django 내장 시스템 (사용자 세션 로그인)
from django.contrib.auth.decorators import login_required             # 로그인한 사용자만 접근 가능하도록 제한
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 암호화, 암호화된 비밀번호와 기본 비밀번호 크로스체크
from django.contrib import messages                                   # Django 내장 시스템 (성공, 오류 등 피드백 전달용)
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt  # csrf_exempt 임포트 추가
from django.http import JsonResponse
from django.db import connection



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
    # 현재 로그인한 사용자의 캐릭터만 조회
    characters = Character.objects.filter(user=request.user)
    
    # 대표 캐릭터 조회 (is_representative가 True인 캐릭터)
    representative_character = characters.filter(is_representative=True).first()
    
    # 대표 캐릭터 이름 가져오기 (없을 경우 "없음"으로 설정)
    representative_character_name = representative_character.name if representative_character else "없음"
    
    # 템플릿에 캐릭터 목록과 대표 캐릭터 이름 전달
    return render(request, 'character_main.html', {
        'characters': characters,
        'representative_character_name': representative_character_name,  # 대표 캐릭터 이름 추가
    })


# 대표 캐릭터 설정
@csrf_exempt  # CSRF 토큰 검증을 비활성화 (보안상 주의 필요)
def Character_Set(request):
    if request.method == 'POST':
        character_id = request.POST.get('character_id')
        try:
            # 모든 캐릭터의 대표 설정을 False로 변경
            Character.objects.filter(user=request.user).update(is_representative=False)
            
            # 선택한 캐릭터를 대표 캐릭터로 설정
            character = Character.objects.get(id=character_id)
            character.is_representative = True  # is_representative를 True로 설정
            character.save()
            
            # 대표 캐릭터 이름 반환
            return JsonResponse({
                'message': '대표 캐릭터로 설정되었습니다.',
                'character_name': character.name  # 대표 캐릭터의 이름 추가
            }, status=200)
        except Character.DoesNotExist:
            return JsonResponse({'error': '캐릭터를 찾을 수 없습니다.'}, status=404)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


# 캐릭터 삭제
@csrf_exempt  # CSRF 토큰 검증을 비활성화 (보안상 주의 필요)
def Character_Delete(request):
    if request.method == 'POST':
        character_id = request.POST.get('character_id')
        try:
            character = Character.objects.get(id=character_id)
            character.delete()
            return JsonResponse({'message': '캐릭터가 삭제되었습니다.'}, status=200)
        except Character.DoesNotExist:
            return JsonResponse({'error': '캐릭터를 찾을 수 없습니다.'}, status=404)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

# 캐릭터 상세정보 페이지
def Character_detail(request, character_id):
    character_object = Character.objects.get(id = character_id)
    return render(request, 'character_detail.html',{'character': character_object})

# 게임 메인페이지
def Game_Main(request):
    return render(request, 'game_main.html')

# 랭킹 조회 페이지
def Game_Rangking(request):
    characters_object = Character.objects.all().order_by('-level')
    request_user = request.user.id
    user_object = Users.objects.get(id = request_user)
    dictionary = {
        'characters': characters_object,
        'user': user_object,
    }
    return render(request, 'game_rangking.html', dictionary)

# 랭킹 페이지에서 방문하기
def Rangking_Detail(request, character_id):
    character_object = Character.objects.get(id = character_id)
    return render(request, 'rangking_detail.html', {'character':character_object})

# 유저 목록 페이지
def Game_User_List(request):
    user_object = Users.objects.all()
    character_object = Character.objects.all()
    dictionary = {'users' : user_object,
                  'characters': character_object,
    }

    return render(request, 'game_user_list.html', dictionary)

# 유저 목록에서 방문하기
def User_List_Visit(request, user_id):
    user_object = Users.objects.get(id = user_id)
    return render(request,'user_list_visit.html', {'user' : user_object})

def Game_Challenge(request):
    return render(request, 'game_challenge.html')

def Game_Shop(request):
    return render(request, 'game_shop.html')

# 전투 페이지 뷰 함수
def Game_battle(request, level):
    user_id = "dbsckdgus"  # 테스트용으로 하드코딩된 user_id, 추후 request.user.username으로 변경 가능

    # DB에서 해당 레벨의 HP, 강한 공격력, 약한 공격력을 가져오기
    with connection.cursor() as cursor:
        cursor.execute("SELECT hp, strong_attack, weak_attack FROM django_challenge_spec WHERE level = %s", [level])
        spec_result = cursor.fetchone()
        if spec_result:
            level_hp = spec_result[0]            # 해당 레벨의 HP
            strong_attack_damage = spec_result[1] # 해당 레벨에서 강한 공격력
            weak_attack_damage = spec_result[2]   # 해당 레벨에서 약한 공격력
        else:
            # 만약 레벨 데이터가 없으면 기본값을 설정
            level_hp = 200
            strong_attack_damage = 50
            weak_attack_damage = 20

    # DB에서 플레이어의 HP를 가져오기 (전투 초기화 시 사용)
    with connection.cursor() as cursor:
        cursor.execute("SELECT HP FROM django_user_spec WHERE user_id = %s", [user_id])
        result = cursor.fetchone()
        if result:
            db_hp = result[0]  # DB에서 가져온 플레이어의 HP 값
        else:
            db_hp = 200  # DB에 값이 없을 경우 기본 HP 설정

    # 세션에 플레이어의 HP와 전투 정보를 설정
    if 'player_hp' not in request.session:
        request.session['player_hp'] = db_hp  # 플레이어의 HP
        request.session['opponent_hp'] = level_hp  # 상대방 HP는 레벨에 맞게 설정
        request.session['battle_logs'] = []
        request.session['turn_counter'] = 1

    player_hp = request.session['player_hp']
    opponent_hp = request.session['opponent_hp']
    battle_logs = request.session['battle_logs']
    turn_counter = request.session['turn_counter']

    battle_result = None  # 전투 결과를 저장할 변수

    if request.method == 'POST':
        attack_type = request.POST.get('attack_type')

        # 플레이어 공격 로직 (레벨에 따른 공격력 적용)
        if attack_type == 'strong':
            player_damage = strong_attack_damage  # 레벨에 따른 강한 공격력
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 강한 공격으로 {player_damage}의 피해를 입혔습니다!")
        else:
            player_damage = weak_attack_damage  # 레벨에 따른 약한 공격력
            battle_logs.append(f"{turn_counter}번째 턴: 플레이어가 약한 공격으로 {player_damage}의 피해를 입혔습니다!")

        opponent_hp -= player_damage
        if opponent_hp <= 0:
            opponent_hp = 0
            battle_result = 'win'  # 승리

        # 상대방 공격 로직 (플레이어가 승리하지 않은 경우에만)
        if opponent_hp > 0:
            opponent_damage = 30  # 상대방 공격은 임의로 설정 (추후 수정 가능)
            battle_logs.append(f"{turn_counter}번째 턴: 상대방이 강한 공격으로 {opponent_damage}의 피해를 입혔습니다!")
            player_hp -= opponent_damage
            if player_hp <= 0:
                player_hp = 0
                battle_result = 'lose'  # 패배

        turn_counter += 1

        request.session['player_hp'] = player_hp
        request.session['opponent_hp'] = opponent_hp
        request.session['battle_logs'] = battle_logs
        request.session['turn_counter'] = turn_counter

    context = {
        'player_hp': player_hp,
        'opponent_hp': opponent_hp,
        'battle_logs': battle_logs,
        'battle_result': battle_result,  # 전투 결과 추가
        'level': level  # 레벨 정보 추가
    }

    return render(request, 'game_battle.html', context)




# 레벨 선택 페이지 뷰 함수
def Game_Challenge(request):
    #user_id = request.user.username  # Django의 사용자 ID(테스트용으로 죽여놈)
    user_id = "dbsckdgus" #테스트 끝나면 삭제

    # SQL 쿼리를 직접 실행하는 방식 (Django ORM을 사용하지 않는 경우)
    with connection.cursor() as cursor:
        cursor.execute("SELECT level FROM django_user_spec WHERE user_id = %s", [user_id])
        cleared_levels = [row[0] for row in cursor.fetchall()]

    # 클리어한 레벨이 없을 경우 기본값으로 1단계를 처리
    if not cleared_levels:
        cleared_levels = [1]


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
    user_id = "dbsckdgus"  # 테스트용으로 하드코딩된 user_id, 추후 request.user.username으로 변경 가능

    # DB에서 사용자의 HP를 가져오기
    with connection.cursor() as cursor:
        cursor.execute("SELECT HP FROM django_user_spec WHERE user_id = %s", [user_id])
        result = cursor.fetchone()
        if result:
            db_hp = result[0]  # DB에서 가져온 HP 값

    # 전투 상태를 초기화
    request.session['player_hp'] = db_hp
    request.session['opponent_hp'] = 211
    request.session['battle_logs'] = []
    request.session['turn_counter'] = 1

    # 초기화 후 해당 레벨의 전투 페이지로 이동
    return redirect('배틀', level=level)