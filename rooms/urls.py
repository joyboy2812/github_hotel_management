from django.urls import path
from . import views

urlpatterns = [
    path('select-hotel/', views.select_hotel, name='select-hotel'),
    path('manage-room/<int:pk>/', views.manage_room, name='manage-room'),
    path('create-room/<int:pk>/', views.create_room, name='create-room'),
    path('update-room/<int:hotel_pk>/<int:room_pk>/', views.update_room, name='update-room'),
    path('delete-room/<int:hotel_pk>/<int:room_pk>/', views.delete_room, name='delete-room'),
]