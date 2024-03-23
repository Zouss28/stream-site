from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import CustomUserCreationForm

# Create your views here.

def login_view(request):
    message =''
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('index')
        message = "Wrong Username or password"
    return render(request, 'login.html', {'message':message})

def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('login')
        
    return render(request, 'signup.html',{
            "form":form
            })
    
def logout_view(request):
    logout(request)
    return redirect('login')