from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('otp',views.generate_otp,name='generate_otp'),
    path('submit_otp',views.submit_otp,name='submit_otp'),
    path('index',views.index_page,name='index'),
    path('password_submission', views.password_submission, name='password_submission'),
    path('media_submission',views.media_submission,name='media_submission'),
    # path('show_password/<int:pid>',views.show_password, name='show_password')
    

]