from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import AstroProfile


def get_theme(request):
    try:
        selected_theme = request.session['selected_theme']
    except:
        request.session.setdefault('selected_theme', 'light')
    
    selected_theme = request.session['selected_theme']
    if selected_theme:
        return HttpResponse(request.session['selected_theme'])

    else:
        request.session.setdefault('selected_theme', 'light')
        return HttpResponse(request.session['selected_theme'])


def toggle_theme(request):
    selected_theme = str(request.session['selected_theme'])
    
    if selected_theme:
        if selected_theme == 'light':
            request.session['selected_theme']  = 'dark'

        elif selected_theme == 'dark':
            request.session['selected_theme']  = 'light'
    
        return HttpResponse(request.session['selected_theme'])

    else:
        selected_theme = get_theme(request)
        return HttpResponse(request.session['selected_theme'])


def sign_up(request):
    if request.method == 'POST':
        # Fetch User Details from Web Page
        username = request.POST.get('username')
        email_address = request.POST.get('emailaddress')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/sign_up.html', {'message': 'Username already exists!'})

        elif password != confirm_password:
            return render(request, 'auth/sign_up.html', {'message': 'Passwords do not match!'})

        elif User.objects.filter(email=email_address).exists():
            return render(request, 'auth/sign_up.html', {'message': "Email address already associated to an account!"})

        # Create a New User instance and Set Attributes
        new_user = User.objects.create_user(
            username=username, 
            email=email_address, 
            password=password
        )
        # Set Is? - Staff
        new_user.is_staff = False
        # Set Is? - Superuser
        new_user.is_superuser = False
        # Save User to Database
        new_user.save()
        
        # Associate user profile object
        AstroProfile.objects.create(user=new_user).save()
        
        # Login the user
        return render(request, 'auth/login.html', {'success_message': 'User successfully created! Please login using the same credentials.'})

    else:
        return render(request, 'auth/sign_up.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        
        try:
            # Authorize user
            user = authenticate(username=username, password=password)

        except Exception as ex:
            print(ex)
            return HttpResponseRedirect(reverse('users:login'), {'message': ex})

        # Handle invalid inputs
        if user is None:
            error_message = "Invalid Username or Password!"
            return render(request, 'auth/login.html', {'message': error_message})
        else:
            # Login user 
            login(request, user)
            return HttpResponseRedirect(reverse('portal:index'))
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portal:index'))
    return render(request, 'auth/login.html')


def user_profile(request):
    return render(request, 'auth/astro.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))