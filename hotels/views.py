from .models import Hotel
from rest_framework.decorators import api_view, permission_classes
from permissions.custom_permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import HotelSerializer


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAdminUser])
def manage_hotel(request):
    hotels = Hotel.objects.all()
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_hotel(request):
    if request.method == 'POST':
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            # Kiểm tra xem có khách sạn nào đã có cùng tên chưa
            hotel_name = serializer.validated_data['hotel_name']
            if Hotel.objects.filter(hotel_name=hotel_name).exists():
                return Response({'error': 'Khách sạn đã tồn tại'}, status=400)

            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_hotel(request, pk):
    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response({'error': 'Không tìm thấy khách sạn'}, status=404)

    if request.method == 'PUT':
        serializer = HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_hotel(request, pk):
    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response({'error': 'Không tìm thấy khách sạn'}, status=404)

    hotel.delete()
    return Response({'message': 'Xóa khách sạn thành công'}, status=204)
