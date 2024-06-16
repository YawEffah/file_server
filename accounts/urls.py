from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_verification_sent/', views.account_verification_sent, name='account_verification_sent'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
