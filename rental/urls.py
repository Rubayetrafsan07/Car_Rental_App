from django.urls import path
from . import views
from .views import CarSearchView
from .views import filtered_car

app_name = 'rental'

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
   # path('manager/',views.manager_dashboard,name='manager_dashboard'),
    path('cars/',views.car_list,name='car_list'),
    path('car/<int:car_id>/', filtered_car, name='filtered_car'),

    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('my_bookings/',views.my_bookings,name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/add_car/', views.add_car, name='add_car'),

    path('manager/bookings/', views.manager_bookings, name='manager_bookings'),
    path('manager/bookings/cancel/<int:booking_id>/', views.cancel_booking_manager, name='cancel_booking_manager'),
    path('change_password/', views.change_password, name='change_password'),

    path('api/search/',CarSearchView.as_view(),name='car_search_api'),
]
