from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta



#Utility function to check if the user is an admin
def is_admin(user):
    return user.groups.filter(name='admin').exists()


#This function registers a user and deactives the account until verified via email
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()
            try:
                send_verification_email(request, user)
                messages.success(request, 'Account successfully created!')
                return redirect(reverse('account_verification_sent'))
            except Exception as e:
                user.delete()  # Clean up by deleting the user if email sending fails
                messages.error(request, 'Account creation unsuccessful! Please try again!')
                return render(request,'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


#This function displays a success message of the email being sent
def account_verification_sent(request):
    return render(request, 'registration/account_verification_sent.html')


#This function sends a verification link to the users email
def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your FileBox Account '
    message = render_to_string('registration/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })
    user.email_user(subject, message)


#This function activates the user's account when the link in the email is clicked
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        # Check if the verification link has expired
        if user.date_joined < timezone.now() - timedelta(minutes=5):
            user.delete()
            return render(request, 'registration/account_activation_error.html')
        else:
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        

#This function handles the login process
def login_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect(reverse('filebox:admin_dashboard'))
        else:
            return redirect(reverse('filebox:user_dashboard'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                # Check if the user is active or not
                if user.is_active == False:
                    return render(request, 'registration/login.html', {
                    'form': form, 
                    'errors': 'Your account is inactive. Please check your email to activate it.'
                })
                login(request, user)
                if is_admin(user):
                    return redirect(reverse('filebox:admin_dashboard'))
                else:
                    return redirect(reverse('filebox:user_dashboard'))
            else:
                return render(request, 'registration/login.html', {
                    'form': form, 
                    'errors': 'Invalid credentials'
                })
    return render(request, 'registration/login.html', {'form': LoginForm()})


#This function logs the user out
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



        
        


