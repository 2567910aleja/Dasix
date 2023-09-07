from django.urls import path
from core.user.views import *


app_name = 'user'

urlpatterns = [
    #Usuario
    path('list/', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    #path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    #path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    ]