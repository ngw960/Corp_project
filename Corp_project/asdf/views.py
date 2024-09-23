from django.shortcuts import render, redirect
from .models import Users



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

