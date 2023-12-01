from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

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
    unmasked_passwords  = [password_obj.password for password_obj in passwords_details]

    medias = Media.objects.all()

    masked_passwords = []

    for password in unmasked_passwords:
        masked_password = '*' *  len(password)
        masked_passwords.append(masked_password)
    
    

    zipped_data = zip(passwords_details, masked_passwords,unmasked_passwords)



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
def media_submission(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        caption = request.POST.get('caption')

        new_media = Media(media=media, caption=caption)
        new_media.save()

        return redirect('home:index')

    return render(request, 'your_template.html')  # Ensure you return a response for GET requests

    