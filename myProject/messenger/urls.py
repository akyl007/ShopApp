from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.indexMessenger, name='index'),
    path('chat_view', views.chat_view, name='chat_view'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat_view'),
    path('send_message/<int:chat_id>/', views.send_message, name='send_message'),
    path('admin_chat/', views.admin_chat_view, name='admin_chat'),
]