from django.urls import path
from django.contrib.auth.views import  LogoutView
from .import views
urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path('password/', views.change_password, name="change_password"),
]
