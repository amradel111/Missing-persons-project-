from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.forms import PasswordResetForm

from user_auth.forms import LoginForm, UserRegistrationForm


def login_view(request):
    """View for user login."""
    # Always log out the user when they visit the login page
    if request.user.is_authenticated:
        logout(request)
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Always set session to expire when browser is closed
                request.session.set_expiry(0)
                
                return redirect('core_app:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'user_auth/login.html', {'form': form})


def register_view(request):
    """View for user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('core_app:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_auth/register.html', {'form': form})


def logout_view(request):
    """View for user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('user_auth:login')


@login_required
def welcome_view(request):
    """Simple welcome view after login."""
    return redirect('core_app:dashboard')


def password_reset_request(request):
    """View for password reset functionality."""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user_auth/password_reset_email.txt"
                    context = {
                        "email": user.email,
                        "domain": request.META['HTTP_HOST'],
                        "site_name": "Missing Persons Finder",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": 'https' if request.is_secure() else 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email, 'noreply@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="user_auth/password_reset.html", context={"form": password_reset_form}) 