from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate , login, logout
from .models import User, Account
import re, os


def profile_update(request, form, user):
    email = form.cleaned_data.get('email')
    name  = form.cleaned_data.get('name')
    if name:
        account = Account.objects.get(user=user)
        account.name = name
        account.save()
    if user.email != email:
        user.email = email
        user.save()
    messages.success(request, "Your data has been saved.")

def change_password(request, form, user):
    password = form.cleaned_data.get('n_pass')
    user.set_password(password)
    user.save()
    logout(request)
    user = authenticate(request, username=user.username, password=password)
    login(request, user)
    messages.info(request, "Your password has been updated.")

def delete_img(path):
    if os.path.isfile(path):
        os.remove(path)

def validEmail(email):
    try:
        validate_email(email)
    except ValidationError as e:
        return False
    else:
        return True

def validUsername(username):
    if re.compile("^[A-Za-z0-9_]+$").match(username):
        return True
    else:
        return False


def validName(name):
    name = str(name)
    if re.compile("^[A-Za-z .-]+$").match(name):
        return True
    else:
        return False
