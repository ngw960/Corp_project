from django.shortcuts import render, redirect
from .models import Users
from django.contrib.auth import login



def Main_Page(request):
    return render(request, "main.html")


def Signup_Page(request):
    return render(request, "signup.html")


def Signup_Action(request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')
    var_name = request.POST.get('input_name')
    var_email = request.POST.get('input_email')

    # 빈 필드가 없는지 검증
    if var_user_id and var_password and var_name and var_email:

        # 입력받은 아이디, 이메일이 db에 존재하는지 검증
        if Users.objects.filter(user_id = var_user_id).exists():
            return redirect('Signup_Page')
    
        if Users.objects.filter(email = var_email).exists():
            return redirect('Signup_Page')
        
        # db에 입력받은 유저 정보 저장
        Users.objects.create(
            user_id = var_user_id,
            password = var_password,
            name = var_name,
            email = var_email
        )
        
        return render(request, "login.html")

    else:
        return redirect('Signup_Page')


def Login_Page(request):
    return render(request, "login.html")


def Login_Action(request):
    # 입력받은 값 정의
    var_user_id = request.POST.get('input_user_id')
    var_password = request.POST.get('input_password')

    # 빈 필드가 없는지 검증
    if var_user_id and var_password:

        select_user = Users.objects.filter(user_id = var_user_id).first()

        if select_user:
      
            if select_user.password == var_password:
                # 사용자를 로그인한다
                login(request, select_user)

                return render(request, 'index.html')

            else:
                return redirect('Login_Page')
        
        else:
            return redirect('Login_Page')
    

def Logout(request):
    request.session.flush()

    return redirect('Index_Page')