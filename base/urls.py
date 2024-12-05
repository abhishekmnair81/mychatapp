from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Remove leading slash here
    path('lobby/', views.lobby, name='lobby'),
    path('room/', views.room),
    path('get_token/', views.getToken),
    path('register/', views.userRegister, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]
