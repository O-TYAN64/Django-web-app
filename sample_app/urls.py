
from django.urls import path
from . import views

app_name = 'sample_app' #django2.0から必要になったnamespace定義
urlpatterns = [
    path('', views.index, name='index'),
]

