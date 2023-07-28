from django.urls import path
from . import views

urlpatterns = [
    path('manage-hotel/', views.manage_hotel, name="api-manage-hotel"),
    path('create-hotel/', views.create_hotel, name="api-create-hotel"),
    path('update-hotel/<int:pk>/', views.update_hotel, name="api-update-hotel"),
    path('delete-hotel/<int:pk>/', views.delete_hotel, name="api-delete-hotel"),
]