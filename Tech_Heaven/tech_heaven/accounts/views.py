from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from products.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def logout_view(request):
    logout(request) 
    return redirect("login")

def register_view(request):
     categories = Category.objects.all()
     if request.user.is_authenticated:
          return redirect('home')
     else:
          if request.method == 'POST':
               username = request.POST.get('username')
               email = request.POST.get('email')
               password = request.POST.get('password')
               confirm_password = request.POST.get('confirm_password')
                
               if password != confirm_password:
                    messages.error(request, 'Passwords does not match')
                    return redirect('register')
               if not username or not email or not password:
                    messages.error(request, 'All data is required')
                    return redirect('register')

               elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already exist')

               elif User.objects.filter(password=password).exists():
                    messages.error(request, 'Password is not valid')

               else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    messages.success(request, "Account created successfully")
                    return redirect('login')
          return render(request, 'pages/register.html', {'categories':categories})

def login_view(request):
     categories = Category.objects.all()
     if request.user.is_authenticated:
          return redirect('home')
     else:
          if request.method == "POST":
               username = request.POST.get('username')
               password = request.POST.get('password')

               if not username or not password:
                    messages.error(request, 'All data is required')
                    return redirect('login')
               
               else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                         login(request, user)
                         return redirect('home')
                    else:
                         messages.error(request, 'Username or password is incorrect')
                         return redirect("login")
     return render(request,'pages/login.html', {'categories':categories})