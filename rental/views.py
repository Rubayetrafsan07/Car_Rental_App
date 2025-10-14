from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import SignUpForm,CarForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Car
from .models import Booking
from django.shortcuts import get_object_or_404
from datetime import datetime,date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views import View


def is_normal_user(user):
     return user.groups.filter(name='NormalUser').exists()
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_admin(user):
    return user.groups.filter(name='AdminGroup').exists() or user.is_superuser

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def dashboard(request):
    is_manager = request.user.groups.filter(name='Manager').exists()
    return render(request, 'dashboard.html', {'is_manager': is_manager})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the session active
            return redirect('rental:dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/login/')
def car_list(request):
    cars= Car.objects.all()
    return render(request,'car_list.html',{'cars':cars})

@login_required(login_url='/login/')
def filtered_car(request,car_id):
    car=get_object_or_404(Car,id=car_id)
    return render(request,'car_filtered.html',{'car':car})

@login_required(login_url='/login/')
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        days = (end_date - start_date).days + 1
        total_price = days * car.price_per_day

        booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        return render(request, 'booking_success.html', {'booking': booking})

    return render(request, 'book_car.html', {'car': car})


@login_required(login_url='/login/')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('car')
    today = date.today()
    return render(request,'my_bookings.html',{'bookings':bookings,'today':today})


@login_required(login_url='/login/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id,user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('rental:my_bookings')

    return render(request,'cancel_booking.html',{'booking':booking})


@login_required(login_url='/login/')
@user_passes_test(is_manager)
def manager_dashboard(request):
    return render(request,'manager_dashboard.html')

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rental:car_list')
    else:
        form = CarForm()

    return render(request, 'add_car.html', {'form': form})


@login_required(login_url='/login/')
@user_passes_test(is_manager)
def manager_bookings(request):
    # Get all bookings made by Normal Users
    bookings = Booking.objects.filter(user__groups__name='NormalUser').select_related('car', 'user')
    return render(request, 'manager_bookings.html', {'bookings': bookings})

@login_required(login_url='/login/')
@user_passes_test(is_manager)
def cancel_booking_manager(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('rental:manager_bookings')
    return HttpResponse("Invalid request")


class CarSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        cars = Car.objects.filter(name__icontains=query)[:5]
        results = [
            {
                'id': car.id,
                'name': car.name,
                'price_per_day': car.price_per_day
            }
            for car in cars
        ]
        return JsonResponse({'results': results})