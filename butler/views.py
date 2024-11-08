from django.shortcuts import render, redirect
from forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

# Index
def index(request):
  return render(request, 'pages/index.html')

def testFunc(request):
  return render(request, "pages/fncTest.html")


# Errors
def error_404(request):
  return render(request, 'pages/examples/404.html')

def error_500(request):
  return render(request, 'pages/examples/500.html')

