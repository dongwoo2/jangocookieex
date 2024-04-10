from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
# Create your views here.

def index(request):
    print(request.COOKIES) # 쿠키 확인
    print(request.session) # 세션 확인
    print(request.session.session_key) # 세션 아이디(키) 확인 세션은 클라이언트를 구분하기 위해 사용
    request.session['now'] = 'value' # input('now 입력:')
    return render(request, 'ex_cookie/index.html', {'cookies':request.COOKIES})


def session_cookie(request):
    response = HttpResponse('세션 쿠키 생성')
    if not request.COOKIES.get('mycookie'):
        cname = 'mycookie'
        cval = timezone.now()
        response.set_cookie(cname, cval) # 세션 쿠키 유효 시간을 설정하지 않았을 때는 세션쿠키가 됨
        
    return response

def permanent_cookie(request):
    response = HttpResponse('영구(permanent) 쿠키 생성')
    if not request.COOKIES.get('mycookie2'):
        cname = 'mycookie'
        cval = timezone.now().day
        response.set_cookie(
            cname,
            cval,
            max_age=60 # 초단위 이므로 60*60*24*365 와 같은 방식으로 설정
        ) # 영구 쿠키(max_age를 설정한 쿠키)
        
    return response

def login(request):
    if request.method == 'GET':
        remember_id = request.COOKIES.get('id','')
        return render(request,'ex_cookie/login.html', {'remember_id': remember_id})
    else:
        id = request.POST['id']
        pw = request.POST['pw']
        # remember = request.POST['remember'] 포스트로 값을 가져올 때  remember 값이 없을수도 있는데 이런식으로 가져오면 오류가 남
        remember = request.POST.get('remember','') # 없을 때는 '' 값으로 나오게 함수를 이용하면 오류 해결
        response = HttpResponse('로그인 성공!')
        if id == pw:
            # 로그인 성공 시 remember를 확인
            request.session['login_user'] = id # ID를 세션에 저장
            if remember == '':
                response.delete_cookie('id')
            else:
                response.set_cookie('id',id, max_age=60*60)
            return response
        else:
            return render(request,'ex_cookie/login.html')
        
from django.shortcuts import redirect, reverse
        
def logout(request):
    request.session.flush()
    response = redirect(reverse('ex_cookie:index'))
    return response