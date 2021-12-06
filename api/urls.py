from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('json/', views.data_to_json, name='json'),
    path('<username>/', views.SingleUserView.as_view(), name='user'),
    path('<str:username>/json', views.data_to_json_by_user, name='user_json'),
]
