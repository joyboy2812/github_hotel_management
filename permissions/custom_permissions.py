from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Kiểm tra xem người dùng đã đăng nhập hay chưa
        if not request.user.is_authenticated:
            return False

        # Kiểm tra xem người dùng có vai trò là "admin" hay không
        return request.user.profile.role.role_name == 'admin'


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.profile.role.role_name == 'manager'


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.profile.role.role_name == 'staff'


class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.profile.role.role_name == 'registered user'
