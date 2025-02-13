from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('api/signup/', views.signup, name='signup'),
    path('api/get_user/', views.get_user, name='get_user'),
    path('api/logout/', views.logout, name='logout'),
    path('api/delete/', views.delete_user, name='delete_user'),
    path('api/activate/<str:token>/', views.activate, name='activate_user'),
    path('api/reset-password/', views.reset_password_request, name='reset_password'),
    path('api/confirm-password-reset/', views.confirm_password_reset, name='confirmation'),
]