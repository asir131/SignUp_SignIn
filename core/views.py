from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')
def signup(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password2')
        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists(): 
                messages.info(request,'Username taken') 
                return redirect('signup')
            else:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.save()
                # return redirect('login')
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request,'Passwords Not Matching')
            return redirect('signup')
       
        
        
        
    return render(request,'signup.html')
    

def signin(request):
     if request.method=="POST":
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        print(Username,Password)
        #check if user has entered correct credentials
        User = authenticate(username=Username,password=Password)
        
        if User is not None:
            login(request,User)
            return redirect("/")
        else: 
          messages.info(request,'Credentials Invalid')   
          return render(request,'signin.html')  
     return render(request,'signin.html')
 
@login_required(login_url='signin')  
def logoutUser(request):
    logout(request)
    return redirect('/signin') 
     