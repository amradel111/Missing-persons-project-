from django.urls import path
from django.contrib.auth import views as auth_views

from user_auth.views import login_view, register_view, logout_view, welcome_view, password_reset_request

app_name = 'user_auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', welcome_view, name='welcome'),
    
    # Password reset URLs
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='user_auth/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='user_auth/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='user_auth/password_reset_complete.html'), 
         name='password_reset_complete'),
]
