from django.shortcuts import render, redirect
from .models import Users, Posts
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



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
            return redirect('회원가입 페이지')
    
        if Users.objects.filter(email = var_email).exists():
            return redirect('회원가입 페이지')
        
        # db에 입력받은 유저 정보 저장
        Users.objects.create(
            user_id = var_user_id,
            password = var_password,
            name = var_name,
            email = var_email
        )
        
        return render(request, "login.html")

    else:
        return redirect('회원가입 페이지')


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
                return redirect('로그인 페이지')
        
        else:
            return redirect('로그인 페이지')
    

def Logout(request):
    request.session.flush()

    return redirect('Index_Page')


@login_required
def Board_Page(request):
    posts_object = Posts.objects.all()

    return render(request, 'board.html', {'posts' : posts_object})


def Post_Writing_Page(request):
    var_name = request.user.name

    return render(request, 'post_writing.html', {"name" : var_name})


def Post_Writing_Action(request):
    var_title = request.POST.get('input_title')
    var_content = request.POST.get('input_content')
    var_author = request.POST.get('input_author')
    user_object = Users.objects.get(id = request.user.id)
    
    if var_title and var_content:

        Posts.objects.create(
            title = var_title,
            content = var_content,
            author = var_author,
            connected_user = user_object
        )

    else:
        return redirect('글 작성 페이지')
        
    return redirect('글쓰기 게시판 페이지')
    

def Post_Detail_Page(request, post_id):
    post_object = Posts.objects.get(id = post_id)

    return render(request, 'post_detail.html', {'post' : post_object})