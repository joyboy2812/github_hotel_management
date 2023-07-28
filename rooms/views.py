from django.shortcuts import render, redirect
from hotels.models import Hotel
from .models import Room
from .forms import RoomForm
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from permissions.custom_permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import RoomSerializer


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAdminUser])
def manage_room(request, pk):
    try:
        hotel = Hotel.objects.get(id=pk)
    except Hotel.DoesNotExist:
        return Response({'error': 'Không tìm thấy khách sạn'}, status=404)

    if request.method == 'GET':
        rooms = hotel.room_set.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_room(request, pk):
    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response({'error': 'Không tìm thấy khách sạn'}, status=404)

    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room_number = serializer.validated_data['room_number']
            existing_room = Room.objects.filter(room_number=room_number, hotel=hotel).exists()
            if existing_room:
                return Response({'error': 'This room_number in this hotel is already in use. Please use a different room_number.'}, status=400)

            serializer.save(hotel=hotel)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except room.DoesNotExist:
        return Response({'error': 'Can not find room'}, status=404)

    if request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except room.DoesNotExist:
        return Response({'error': 'Can not find room'}, status=404)

    if request.method == 'DELETE':
        room.delete()
        return Response({'message': 'Xóa khách sạn thành công'}, status=204)
