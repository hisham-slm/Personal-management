from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import json
from home.decorators import auth_user
from home.models import Media, Password


# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def generate_otp(request):
    otp = randint(1000, 9999)
    print(otp)
    request.session['generated_otp'] = otp
    msg = f"Your generated OTP for your Personal Website Login is {otp}"


    send_mail("Personal Website", msg, settings.EMAIL_HOST_USER, ['hishamsalam350@gmail.com'], fail_silently=False)
    
    return render(request, 'home/enter_otp.html')

from django.shortcuts import render, redirect


def submit_otp(request):
    if request.method == 'POST':   
        otp_entered = request.POST.get('otp') 

        generated_otp = request.session.get('generated_otp', None)

        if int(otp_entered) == int(generated_otp):
            request.session['user'] = 'user'
            generated_otp = randint(1111,99999)
            return redirect('home:index')
            
        else:
            msg = "Wrong OTP"
            return render(request, 'home/enter_otp.html',{'msg':msg})
    else:
        msg = 'Something Went Wrong'
        return render(request, 'home/enter_otp.html',{'msg':msg})


@auth_user
def index_page(request):
    passwords_details = Password.objects.all()
    title = [password_obj.title for password_obj in passwords_details]
    unmasked_passwords  = [password_obj.password for password_obj in passwords_details]
    username  = [password_obj.username for password_obj in passwords_details]
    masked_passwords = []

    for password in unmasked_passwords:
        masked_password = '*' *  len(password)
        masked_passwords.append(masked_password)
    
    medias = Media.objects.all()
    

    
    zipped_data = []

    zipped_data = json.dumps({
        'title': title,
        'username': username,
        'unsmasked_password':unmasked_passwords,
        'masked_password': masked_passwords
    })  



    return render(request,'home/index.html',{'zipped_data': zipped_data,"medias":medias})

@auth_user
def password_submission(request):
    if request.method == 'POST':
        title = request.POST['title']
        username = request.POST['username']
        password = request.POST['password']


        new_password = Password(
            title = title,
            username =  username,
            password =  password
        )

        new_password.save()

        msg = 'New password added'

        return redirect('home:index')
    
    else:
        msg = "Something went wrong"
        return redirect('home:index')
    

@auth_user
def update_password(request):
    if request.method == 'POST':
        title = request.POST['title']
        username = request.POST['username']
        password = request.POST['password']
    password_details = Password.objects.get(title = title)

    password_details.title = title
    password_details.username = username
    password_details.password = password

    password_details.save()

    return redirect('home:index')

@auth_user
def delete_password(request):
    if request.method == 'POST':
        title = request.POST['title']

    password_detail = Password.objects.get(title = title)

    password_detail.delete()
    return redirect('home:index')



@auth_user
def media_submission(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        caption = request.POST.get('caption')

        new_media = Media(media=media, caption=caption)
        new_media.save()

        return redirect('home:index')

    



@auth_user
def media_deletion(request):
    if request.method == 'POST':
        media_id = request.POST['media']
        media_want_to_be_delete = Media.objects.get(id=media_id)

        media_want_to_be_delete.delete()
    
    return redirect('home:index')


def clear_session(request):
    request.session.flush() 
    return  render(request, 'home/enter_otp.html')