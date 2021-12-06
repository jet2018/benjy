from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostData, name='all'),
    path('data', views.ViewAllStatistics.as_view(), name='all'),
    path('login', views.fake_login, name='login'),
    path('register', views.fake_register, name='register'),
    path('logout', views.fake_logout, name='logout'),
]
