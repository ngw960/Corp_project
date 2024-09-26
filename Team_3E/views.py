from django.shortcuts import render, redirect                         # 렌더링, 리디렉션
from Team_3E.models import Users                              # DB 모델
from django.contrib.auth import login                                 # Django 내장 시스템 (사용자 세션 로그인)
from django.contrib.auth.decorators import login_required             # 로그인한 사용자만 접근 가능하도록 제한
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 암호화, 암호화된 비밀번호와 기본 비밀번호 크로스체크
from django.contrib import messages                                   # Django 내장 시스템 (성공, 오류 등 피드백 전달용)

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
    var_user_id  = request.POST.get('input_user_id')
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
    #if not check_password(var_password, select_user.password):
    if select_user.password == var_password:
        messages.error(request, '비밀번호가 일치하지 않습니다.')
        return redirect('로그인')

    # 유저 로그인
    login(request, select_user)
    messages.success(request, f'{var_user_id}님, 환영합니다!')
    return render(request, 'index.html')

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
