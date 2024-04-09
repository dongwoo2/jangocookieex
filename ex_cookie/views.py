from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
# Create your views here.

def index(request):
    print(request.COOKIES)
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
        return render(request,'ex_cookie/login.html')
    else:
        id = request.POST['id']
        pw = request.POST['pw']
        # remember = request.POST['remember'] 포스트로 값을 가져올 때  remember 값이 없을수도 있는데 이런식으로 가져오면 오류가 남
        remember = request.POST.get('remember','') # 없을 때는 '' 값으로 나오게 함수를 이용하면 오류 해결
        response = HttpResponse('로그인 성공!')
        if id == pw:
            return response
        else:
            return render(request,'ex_cookie/login.html')