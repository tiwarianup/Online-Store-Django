from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.conf.urls.static import static
from django.conf import settings

from .forms import ContactForm, LoginForm, RegisterForm

User = get_user_model()

def homepage(request):
    context = {
        "title": "Homepage",
        "content": "This is some homepage content."
    }
    if request.user.is_authenticated():
        context['premiumContent'] = "This can only be viewed when logged In."
    return render(request, "homepage.html", context)

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