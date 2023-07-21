from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from hotels.models import Hotel
from .models import Room
from .forms import RoomForm
from django.contrib import messages


# Create your views here.


def has_admin_role(user):
    return user.profile.role.role_name == 'admin' or user.profile.role.role_name == 'manager' or user.profile.role.role_name == 'staff'


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def select_hotel(request):
    hotels = Hotel.objects.all()
    context = {
        'hotels': hotels,
    }
    return render(request, 'rooms/select_hotel.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def manage_room(request, pk):
    hotel = Hotel.objects.get(id=pk)
    rooms = hotel.room_set.all()
    context = {
        'hotel': hotel,
        'rooms': rooms,
    }
    return render(request, 'rooms/manage_room.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def create_room(request, pk):
    hotel = Hotel.objects.get(id=pk)
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data['room_number']
            existing_room = Room.objects.filter(room_number=room_number, hotel=hotel).exists()
            if existing_room:
                messages.error(request, 'This room_number in this hotel is already in use. Please use a different room_number.')
            else:
                room = form.save(commit=False)
                room.hotel = hotel
                room.save()
                return redirect('manage-room', pk=hotel.id)
    context = {
        'form': form,
    }
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def update_room(request, hotel_pk, room_pk):
    room = Room.objects.get(id=room_pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('manage-room', pk=hotel_pk)
    context = {
        'form': form,
    }
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def delete_room(request, hotel_pk, room_pk):
    room = Room.objects.get(id=room_pk)
    if request.method == 'POST':
        room.delete()
        return redirect('manage-room', pk=hotel_pk)
    context = {
        'room': room,
        'hotel_pk': hotel_pk,
    }
    return render(request, 'rooms/delete_room.html', context)
