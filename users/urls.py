from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='api-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('register/', views.register_user, name='api-register'),
    path('logout/', views.logout_user, name='api-logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('manage-profile/', views.manage_profile, name='api-manage-profile'),
    path('create-staff/', views.create_staff, name='api-create-staff'),
    path('update-profile/<int:pk>/', views.update_profile, name='api-update-profile'),
    path('delete-profile/<int:pk>/', views.delete_profile, name='api-delete-profile')
]