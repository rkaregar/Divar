from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url=reverse_lazy('ads:home')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url=reverse_lazy('users:password_change_done')), name='change-password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
    path('activation/<slug:username>/', MemberActivationView.as_view(), name='activation'),
    path('signup/', MemberCreationView.as_view(), name='signup'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
]