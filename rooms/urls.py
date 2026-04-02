from django.urls import path
from . import views

app_name = 'rooms'  # Keep the app_name as 'rooms' for consistency with existing templates

urlpatterns = [
    path('', views.room_list, name='room_list'),  # This will show table list
    path('<int:room_id>/', views.room_detail, name='room_detail'),  # Table detail
    path('<int:room_id>/reserve/', views.book_room, name='book_room'),  # Make reservation
    path('reservation/<int:booking_id>/', views.booking_detail, name='booking_detail'),  # Reservation detail
    path('my-reservations/', views.my_bookings, name='my_bookings'),  # User's reservations
    path('cancel-reservation/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # Cancel reservation
    path('check-availability/', views.check_availability, name='check_availability'),  # Check table availability
]