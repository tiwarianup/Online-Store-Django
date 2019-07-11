from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    fullname    = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your full name"
            })
        )
    email       = forms.EmailField(
        widget=forms.EmailInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your Email Id"
            })
    )
    content     = forms.CharField(
        widget=forms.Textarea(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Please write your message here"
            })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email must be a Gmail address only.")

        return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your username"
            })
        )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your password"
            })
        )
User = get_user_model()
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your username"
            })
        )
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your username"
            })
        )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your password"
            })
        )
    confirmPassword = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your password again"
            }),
        label='Confirm Password'
        )

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        confirmPassword = self.cleaned_data.get("confirmPassword")
        if password != confirmPassword:
            raise forms.ValidationError("Passwords must match")
        return data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("This username is already taken. Try another.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email is already taken. Try another.")
        return email