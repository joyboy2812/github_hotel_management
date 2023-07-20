from django.shortcuts import render, redirect
from .models import Hotel
from .forms import HotelForm
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


def has_admin_role(user):
    return user.profile.role.role_name == 'admin'


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def manage_hotel(request):
    hotels = Hotel.objects.all()
    role = 'admin'
    context = {
        'role': role,
        'hotels': hotels,
    }
    return render(request, 'hotels/manage_hotel.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def create_hotel(request):
    form = HotelForm()
    role = 'admin'

    context = {
        'form': form,
        'role': role
    }

    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-hotel')

    return render(request, 'hotels/hotel_form.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def update_hotel(request, pk):
    hotel = Hotel.objects.get(id=pk)
    form = HotelForm(instance=hotel)
    role = 'admin'

    context = {
        'form': form,
        'role': role,
    }

    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('manage-hotel')

    return render(request, 'hotels/hotel_form.html', context)


@login_required(login_url='login')
@user_passes_test(has_admin_role, login_url='login')
def delete_hotel(request, pk):
    hotel = Hotel.objects.get(id=pk)
    role = 'admin'

    context = {
        'role': role,
        'hotel': hotel,
    }

    if request.method == 'POST':
        hotel.delete()
        return redirect('manage-hotel')

    return render(request, 'hotels/delete_template.html', context)
