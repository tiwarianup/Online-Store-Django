from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control col-md-5", 
            "placeholder":"Your Email Id"
            }))

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