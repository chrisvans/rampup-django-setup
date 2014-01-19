from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def login_view(request):
    
    # If the method is post, the user has submitted a username and password and we
    # need to authenticate them.
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)
            return render(request, 'users/login.html', {})

        else:
            return render(request, 'users/login.html', 
                {
                'message': "The credentials provided were incorrect.  If you don't have an account please register.",
                })

    # If the request.method is not 'POST', then the user has not submitted anything.
    else:
        return render(request, 'users/login.html', {})

def registration_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(username=username, email=email, password=password)

        message = 'Successfully registered as ' + username + '!  Please login.'

        return render(request, 'users/login.html',
            {
            'message': message,
            })

    else:
        return render(request, 'users/register.html', {})

def logout_view(request):
    logout(request)

    message = "Now logged out."

    return redirect('/', message=message)
