from django.urls import path
from . import views

urlpatterns = [
    path('manage-hotel/', views.manage_hotel, name="manage-hotel"),
    path('create-hotel/', views.create_hotel, name="create-hotel"),
    path('update-hotel/<int:pk>/', views.update_hotel, name="update-hotel"),
    path('delete-hotel/<int:pk>/', views.delete_hotel, name="delete-hotel"),
]