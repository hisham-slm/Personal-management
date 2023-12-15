from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('otp',views.generate_otp,name='generate_otp'),
    path('submit_otp',views.submit_otp,name='submit_otp'),
    path('index',views.index_page,name='index'),
    path('password_submission', views.password_submission, name='password_submission'),
    path('update_password', views.update_password, name='update_password'),
    path('delete_password', views.delete_password, name='delete_password'),
    path('media_submission',views.media_submission,name='media_submission'),
    path('clear_session',views.clear_session, name='clear_session'),
    # path('show_password/<int:pid>',views.show_password, name='show_password')
    

]