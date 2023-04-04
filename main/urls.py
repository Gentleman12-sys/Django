from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('poster/<int:id>', views.edit, name='poster'),
    path('delete/<int:id>', views.del_post, name='del_post'),
    path('user/<int:id>', views.user, name='user'),
    path('delete/user', views.del_usr, name='del_usr'),
    path('addpost', views.addpost, name='addpost')
]