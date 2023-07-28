from django.urls import path
from . import views

urlpatterns = [
    path('manage-room/<int:pk>/', views.manage_room, name='api-manage-room'),
    path('create-room/<int:pk>/', views.create_room, name='api-create-room'),
    path('update-room/<int:pk>/', views.update_room, name='api-update-room'),
    path('delete-room/<int:pk>/', views.delete_room, name='api-delete-room'),
]