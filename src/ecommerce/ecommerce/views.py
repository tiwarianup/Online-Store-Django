from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.conf.urls.static import static
from django.conf import settings

from .forms import ContactForm, LoginForm, RegisterForm

User = get_user_model()

def homepage(request):
    #this is homepage view
    context = {
        "title": "Homepage",
        "content": "This is some homepage content."
    }
    if request.user.is_authenticated():
        context['premiumContent'] = "This can only be viewed when logged In."
    return render(request, "homepage.html", context)

def loginpage(request):
    #this is login page view
    form = LoginForm(request.POST or None)
    context = {
        "title": "Login to proceed",
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context["form"] = LoginForm()
            return redirect("/")
        else:
            print("Error")
    
    return render(request, "auth/login.html", context)

def registerpage(request):
    # this is registerpage view
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
    
    return render(request, "auth/register.html", context)

def contactpage(request):
    print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    print(settings.STATIC_URL)
    print(settings.STATIC_ROOT)
    contactForm = ContactForm(request.POST or None)
    if contactForm.is_valid():
        senderName = contactForm.cleaned_data.get("fullname")
        senderEmail = contactForm.cleaned_data.get("email")
        message = contactForm.cleaned_data.get("content")
        print(senderName, senderEmail, message)
        contactForm = ContactForm()

    context = {
        "title": "Contact Page",
        "content": "This is some contact page content.",
        "form": contactForm
    }
    return render(request, "contactpage.html", context)