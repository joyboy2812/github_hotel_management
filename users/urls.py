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
]