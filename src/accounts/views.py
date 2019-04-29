from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from .utils import *
from django.contrib import messages
from .models import User, Account
from secretmessages.models import Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def pp_upload_view(request, username):
    if request.user.username != username:
        messages.warning(request, 'You are not authorized to change other user settings')
        return HttpResponseRedirect('/not-authorized/')
    template_name = 'accounts/pp_change.html'
    form = PhotoUploadForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            account = Account.objects.get(user=request.user)
            photo   = form.cleaned_data.get('image')
            if account.pp:
                delete_img(account.pp.path)
            account.pp = photo
            account.save()
            messages.success(request, 'Photo uploaded successfully')
            return HttpResponseRedirect('/accounts/' + str(request.user.username) + "/settings/")
    contex = {
        'form': form,
        'active': 'active_link'
    }
    return render(request, template_name, contex)








@login_required
def settings_view(request, username):
    if request.user.username != username:
        messages.warning(request, 'You are not authorized to change other user settings')
        return HttpResponseRedirect('/not-authorized/')

    template_name = 'accounts/settings.html'
    user = request.user
    action = request.GET.get('action')
    s1, s2, s3, form = None, None, None, None
    if action:
        if action == 'change':
            form = ChangePasswordForm(user, request.POST or None)
            s2 = 's2'
        elif action == 'delete':
            form = DeleteForm(request.POST or None)
            s3 = 's3'
        elif action == 'edit':
            form = EditForm(user, request.POST or None)
            s1 = 's1'
    else:
        action = 'default'

    if request.method == "POST":
        if action and form.is_valid():
            if action == 'change':
                change_password(request, form, user)
            elif action == 'delete':
                logout(request)
                user.delete()
                return HttpResponseRedirect('/')
            elif action == 'edit':
                profile_update(request, form, user)
            return HttpResponseRedirect('/accounts/' + str(user.username) + "/settings/")
    contex = {
        'form': form,
        's1': s1, 's2': s2, 's3': s3,
        'action': action
    }
    return render(request, template_name, contex)











@login_required
def profile_view(request, username):
    if request.user.username != username:
        messages.warning(request, 'You are not authorized to perform the action.')
        return HttpResponseRedirect('/not-authorized/')
    template_name = 'accounts/profile.html'
    account       = Account.objects.get(user=request.user)
    page = request.GET.get('page', 1)
    
    #favourites = Message.objects.all().filter(user=request.user).filter(is_fav=True)
    tab = request.GET.get('tab')
    tab1, tab2, tab3  = '', '', ''
    
    inbox      = None
    favourites = None
    sent       = None
    if tab:
        if tab == 'messages':
            tab1 = 'tab_menu_active'
            paginator  = Paginator(Message.objects.all().filter(user=request.user), 20)
            try:
                inbox = paginator.page(page)
            except PageNotAnInteger:
                inbox = paginator.page(1)
            except EmptyPage:
                inbox = paginator.page(paginator.num_pages)
        elif tab == 'favourites':
            tab2 = 'tab_menu_active'
            paginator  = Paginator(Message.objects.all().filter(user=request.user).filter(is_fav=True), 10)
            try:
                favourites = paginator.page(page)
            except PageNotAnInteger:
                favourites = paginator.page(1)
            except EmptyPage:
                favourites = paginator.page(paginator.num_pages)
        elif tab == 'sent':
            tab3 = 'tab_menu_active'
            paginator  = Paginator(Message.objects.all().filter(sender=request.user.username), 10)
            try:
                sent = paginator.page(page)
            except PageNotAnInteger:
                sent = paginator.page(1)
            except EmptyPage:
                sent = paginator.page(paginator.num_pages)
    else:
        tab1 = 'tab_menu_active'
        tab = 'messages'
        paginator  = Paginator(Message.objects.all().filter(user=request.user), 20)
        try:
            inbox = paginator.page(page)
        except PageNotAnInteger:
            inbox = paginator.page(1)
        except EmptyPage:
            inbox = paginator.page(paginator.num_pages)
    
    contex = {
        'profile_active': 'active',
        'account': account,
        'tab1': tab1, 'tab2': tab2, 'tab3': tab3, 'tab': tab,
        'inbox': inbox, 'favourites': favourites, 'sent': sent
    }
    return render(request, template_name, contex)





def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are logged in!')
        return HttpResponseRedirect('/not-authorized/')
    next = request.GET.get('next', '/')
    template_name = 'accounts/login.html'
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            usr    = form.cleaned_data.get('username')
            if validEmail(usr):
                get_user = get_object_or_404(User, email=usr)
                usr = get_user.username
            passwd = form.cleaned_data.get('password')
            user   = authenticate(request, username=usr, password=passwd)
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            if next != '/':
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/accounts/' + str(usr) + '/')
    contex = {
        'form': form,
        'login_active': 'active'
    }
    return render(request, template_name, contex)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')













def register_view(request):
    template_name = 'accounts/register.html'
    info = ""
    if request.user.is_authenticated:
        messages.warning(request, 'You are logged in!')
        return HttpResponseRedirect('/not-authorized/')
    if request.method == "POST":
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        re_password = request.POST.get('re_password')
        err = 0
        if username and email and password and re_password:
            # username validation
            if len(username) < 3:
                err += 1
                info = "Username is too small"
            if len(username) > 32:
                err += 1 
                info = "Username is too long"
            if not validUsername(username):
                err += 1
                info = "Username contains invalid characters"

            usr = User.objects.filter(username=username)
            if usr.exists():
                err += 1
                info = "Username already taken!"

            # email validation
            if not validEmail(email):
                err += 1
                info = "Invalid email"
            eml = User.objects.filter(email=email)
            if eml.exists():
                err += 1
                info = "E-mail is already registered!"

            # password validation
            if len(password) < 6:
                err += 1
                info = "Password is too small"
            if password != re_password:
                err += 1
                info = "Password didn't match"
        else:
            err += 1
            info = "You need to fill every field to register"
        if err == 0:
            user = User()
            user.username = username
            user.email    = email
            user.set_password(password)
            user.save()
            account = Account()
            account.user = user
            account.save()
            messages.success(request, 'Congrats! You are successfully registered.')
            user = authenticate(request, username=user.username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    
    contex = {
        'info': info,
        'register_active': 'active'
    }
    return render(request, template_name, contex)


