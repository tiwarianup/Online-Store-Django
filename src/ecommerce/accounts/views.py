from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.conf.urls.static import static
from django.conf import settings
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

User = get_user_model()

def guestRegisterPage(request):
    form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirectPath = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        newGuestEmail = GuestEmail.objects.create(email=email)
        request.session['guestEmailId'] = newGuestEmail.id
        if is_safe_url(redirectPath, request.get_host()):
            return redirect(redirectPath)
        else:
            return redirect("/register/")
    return redirect("/register/")

def loginpage(request):
    form = LoginForm(request.POST or None)
    context = {
        "title": "Login to proceed",
        "form": form
    }

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirectPath = next_ or next_post or None

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #context["form"] = LoginForm()

            try:
                del request.session['guestEmailId']
            except:
                pass
            
            if is_safe_url(redirectPath, request.get_host()):
                return redirect(redirectPath)
            else:
                return redirect("/")
        else:
            print("Error")
    
    return render(request, "accounts/login.html", context)

def registerpage(request):
    form = RegisterForm(request.POST or None)
    context = {
        "title": "Register a new account",
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")       
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        newUser = User.objects.create_user(username, email, password)
        print(newUser)
        context["form"] = RegisterForm()
    
    return render(request, "accounts/register.html", context)

