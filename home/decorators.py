from django.shortcuts import render,redirect


def auth_user(function):
    def wrapper(request,*args,**kwargs):
        if 'user' in request.session:
            return function(request,*args,**kwargs) 
        else:
            return redirect('home:generate_otp')
    
    return wrapper