from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import Profile
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


# Create your views here.


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid")

    return redirect('home')


def home(request):
    context = {
    }
    return render(request, 'users/home.html', context)


def login_user(request):
    page = 'login'
    context = {
        'page': page
    }

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect!')

    return render(request, 'users/login_register.html', context)


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} '
                                  f'inbox and click on received activation link to confirm and complete the '
                                  f'registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed correctly')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CustomUserCreationForm()
    page = 'register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_user = User.objects.filter(email=email).exists()
            if existing_user:
                messages.error(request, 'This email is already in use. Please use a different email.')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.username = user.username.lower()
                user.save()
                activate_email(request, user, form.cleaned_data.get('email'))
                return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration!')
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'User logged out!')
    return redirect('login')
