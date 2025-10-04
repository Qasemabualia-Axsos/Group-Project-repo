from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from movies.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    movie=Movies.objects.all()
    actor=Actors.objects.all()
    director=Directors.objects.all()
    data={
        'Movies':movie,
        'Actors':actor,
        'Directors':director
    }
    return render (request,'home.html',data)

def login_page(request):

    return render (request,'login.html')

def register_page(request):

    return render (request,'register.html')

def login(request):
    if request.method=='POST':
        user=Users.objects.filter(email=request.POST.get('email')).first()
        
        if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
                request.session['userid']=user.id
                request.session['first_name']=user.first_name
                # messages.success(request,'Successfully logged in !',extra_tags='login')
                return redirect('movies:dashboard')
        else:
            messages.error(request,'Invalid email or password',extra_tags='login')
            return redirect('accounts:login_page')

def register(request):
    if request.method=='POST':
        errors=Users.objects.user_validator(request.POST)
        if len(errors)>0:
            for feild ,error in errors.items():
                messages.error(request,error,extra_tags=feild)
            return redirect('accounts:register_page')

        else:
            password=request.POST.get('password')
            pw_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    
        Users.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                password=pw_hash
        )
        request.session['first_name']=request.POST.get('first_name')
        messages.success(request,'Successfully create User',extra_tags='register')
        return redirect('accounts:register_page')
    return redirect('accounts:register_page')


def user_profile(request):
    if 'userid' not in request.session:
        return redirect('login_page')
    user=Users.objects.get(id=request.session['userid'])
    data={
        'user':user
    }
    return render (request,'user_profile.html',data)



def edit_profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = Users.objects.get(id=request.session['userid'])
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        if email: user.email = email

        user.save()
        # return updated data
        return JsonResponse({
            "status": "success",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        })

    return JsonResponse({"status": "failed", "message": "Invalid request"})

@login_required
def delete_profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = Users.objects.get(id=request.session['userid'])
        user.delete()
        request.session.flush()  # clear session
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed", "message": "Invalid request"})
