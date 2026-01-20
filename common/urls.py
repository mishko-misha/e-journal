from django.urls import path

from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('user/<int:user_id>',views.user_view,name='user_view'),
]