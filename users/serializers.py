from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True)  # Chỉ dùng để nhận dữ liệu từ request, không lưu vào database

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}  # Ẩn trường password trong response

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.get('password', None)

        if password and password != confirm_password:
            raise serializers.ValidationError("Mật khẩu không khớp.")

        user = User.objects.create_user(**validated_data)
        return user
