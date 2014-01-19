from django.contrib.auth import authenticate, login
from django.shortcuts import render

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
                'error_message': "The credentials provided were incorrect.  If you don't have an account please register.",
                })

    # If the request.method is not 'POST', then the user has not submitted anything.
    else:
        return render(request, 'users/login.html', {})

def registration_view(request):
    return render(request, 'users/register.html', {})