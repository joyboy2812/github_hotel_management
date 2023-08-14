from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import CustomUserCreationForm
from .models import Profile, Role, Booking, BookingDetail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, CreateStaffSerializer, UpdateProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.conf import settings
from permissions.custom_permissions import IsAdminUser, IsManagerUser, IsRegisteredUser
from rooms.models import Room
from datetime import datetime


# Create your views here.


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account")
        return redirect('api-login')
    else:
        messages.error(request, "Activation link is invalid")

    return redirect('home')


def home(request):
    context = {
    }
    return render(request, 'users/home.html', context)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'expires_in': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        }

        login(request, user)

        return Response(response_data)
    else:
        return Response({"message": "Invalid credentials"}, status=400)


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} '
                                  f'inbox and click on received activation link to confirm and complete the '
                                  f'registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed correctly')


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        existing_user = User.objects.filter(email=email).exists()
        if existing_user:
            return Response({'error': 'This email is already in use. Please use a different email.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.create(serializer.validated_data)
            user.is_active = False
            user.username = user.username.lower()
            user.save()
            activate_email(request, user, serializer.validated_data.get('email'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        # Thu hồi token
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Đăng xuất thành công."}, status=200)
    except Exception as e:
        return Response({"message": "Đăng xuất thất bại."}, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser | IsManagerUser])
def manage_profile(request):
    if request.user.profile.role.role_name == 'admin':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
    elif request.user.profile.role.role_name == 'manager':
        role = Role.objects.get(role_name='staff')
        profiles = Profile.objects.filter(role=role)
        serializer = ProfileSerializer(profiles, many=True)
    else:
        return Response({'error': 'You do not have permission to view profile list.'}, status=403)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsManagerUser])
def create_staff(request):
    serializer = CreateStaffSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username'].lower()
        password = serializer.validated_data['password']

        # Kiểm tra xem username đã tồn tại trong hệ thống chưa
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo user mới
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.get(user=user)
        staff_role = Role.objects.get(role_name='staff')
        profile.role = staff_role
        profile.save()

        # Response
        return Response({'message': 'Staff user created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser | IsManagerUser])
def update_profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except Profile.DoesNotExist:
        return Response({"message": "Profile not found"}, status=404)

        # Check if the request contains 'username' and 'role_name' fields
    if 'username' not in request.data or 'role_name' not in request.data:
        return Response({"message": "Username and role_name fields are required"}, status=400)

    new_username = request.data['username']

    try:
        # Check if the new username is unique
        if User.objects.filter(username=new_username).exists():
            return Response({"message": "Username already exists"}, status=400)

        # Update User's username
        profile.user.username = new_username
        profile.user.save()

        # Update Role's role_name
        profile.role.role_name = request.data['role_name']
        profile.role.save()

        # Serialize and return updated Profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(['PUT'])
@permission_classes([IsRegisteredUser])
def update_username(request, pk):
    if request.user.profile.id == pk:
        try:
            profile = Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=404)

            # Check if the request contains 'username' and 'role_name' fields
        if 'username' not in request.data:
            return Response({"message": "Username fields are required"}, status=400)

        new_username = request.data['username']

        try:
            # Check if the new username is unique
            if User.objects.filter(username=new_username).exists():
                return Response({"message": "Username already exists"}, status=400)

            # Update User's username
            profile.user.username = new_username
            profile.user.save()

            # Serialize and return updated Profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
    else:
        return Response({"message": "You can not change other username"}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAdminUser | IsManagerUser])
def delete_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response({'error': 'Can not find profile'}, status=404)

    profile.delete()
    return Response({'message': 'Delete success'}, status=204)


@api_view(['POST'])
@permission_classes([IsRegisteredUser])
def create_booking_detail(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({"message": "Room not found"}, status=404)

    try:
        booking = request.user.profile.booking_set.get(is_booked=False)
    except Booking.DoesNotExist:
        booking = Booking.objects.create(profile=request.user.profile)

    check_in_date_str = request.data.get('check_in_date')
    check_out_date_str = request.data.get('check_out_date')

    if not check_in_date_str or not check_out_date_str:
        return Response({'message': 'check_in_date and check_out_date fields are required'}, status=400)

    check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d %H:%M:%S')
    check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d %H:%M:%S')

    if check_out_date <= check_in_date:
        return Response({'message': 'check_out_date must be greater than check_in_date'}, status=400)

    booking_detail = BookingDetail(booking=booking, room=room, check_in_date=check_in_date,
                                   check_out_date=check_out_date)
    booking_detail.price = room.price
    overlapping_booking_details = BookingDetail.objects.filter(
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date,
        is_booked=True)

    conflicting_booking_details = BookingDetail.objects.filter(
        booking=booking,
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date,
    )

    if overlapping_booking_details:
        return Response({'message': 'This booking period overlaps with existing booking(s)'}, status=400)

    if conflicting_booking_details:
        return Response({'message': 'You already have booked this room in this period'}, status=400)

    booking_detail.save()

    return Response({'message': 'You have succeed create booking detail. Please save booking to finish your booking'},
                    status=204)


@api_view(['PUT'])
@permission_classes([IsRegisteredUser])
def save_booking(request):
    try:
        booking = request.user.profile.booking_set.get(is_booked=False)
    except Booking.DoesNotExist:
        return Response({'message': 'You have no booking right now'})

    bookingDetails = booking.bookingdetail_set.all()
    for booking_detail in bookingDetails:
        conflicting_booking_details = BookingDetail.objects.filter(
            room=booking_detail.room,
            check_in_date__lt=booking_detail.check_out_date,
            check_out_date__gt=booking_detail.check_in_date,
            is_booked=True
        ).exclude(id=booking_detail.id)
        if conflicting_booking_details:
            overlap_message = f'This {booking_detail.room} in {booking_detail.check_in_date} and {booking_detail.check_out_date} overlaps with existing booking(s)'
            return Response({'message': overlap_message}, status=400)

    for booking_detail in bookingDetails:
        booking_detail.is_booked = True
        booking_detail.save()
    booking.is_booked = True
    booking.save()
    return Response({'message': 'You have successfully booked'}, status=204)