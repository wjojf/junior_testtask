from django.contrib import admin
from django.urls import path, include
from base import views as base_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', base_views.HomeView.as_view(), name='home'),
    
    path('login/', base_views.loginPage, name='login'),
    path('logout/', base_views.logoutUser, name='logout'),
    path('register', base_views.registerPage, name='register'),
    
    path(
        'course/<int:course_id>',
        base_views.CourseView.as_view(),
        name='course'
    ),
    
]