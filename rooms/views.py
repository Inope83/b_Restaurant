from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Table, TableType, Reservation, TableImage
from .forms import RoomSearchForm, BookingForm
from datetime import date, timedelta, datetime, time

def room_list(request):
    form = RoomSearchForm(request.GET or None)
    tables = Table.objects.filter(is_active=True)
    
    if form.is_valid():
        reservation_date = form.cleaned_data.get('reservation_date')
        reservation_time = form.cleaned_data.get('reservation_time')
        party_size = form.cleaned_data.get('party_size')
        table_type = form.cleaned_data.get('table_type')
        
        # Filter by table type
        if table_type:
            tables = tables.filter(table_type=table_type)
        
        # Filter by capacity
        if party_size:
            tables = tables.filter(table_type__max_capacity__gte=party_size)
        
        # Filter by availability
        if reservation_date and reservation_time:
            available_tables = []
            for table in tables:
                if table.is_available(reservation_date, reservation_time):
                    available_tables.append(table.id)
            tables = tables.filter(id__in=available_tables)
    
    # Pagination
    paginator = Paginator(tables, 6)  # Show 6 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'table_types': TableType.objects.all(),
    }
    return render(request, 'rooms/room_list.html', context)

def room_detail(request, room_id):
    table = get_object_or_404(Table, id=room_id, is_active=True)
    images = table.images.all()
    
    # Check availability for next 30 days
    availability_data = []
    current_date = date.today()
    for i in range(30):
        check_date = current_date + timedelta(days=i)
        # Check availability for dinner time (7 PM)
        dinner_time = time(19, 0)
        is_available = table.is_available(check_date, dinner_time)
        availability_data.append({
            'date': check_date,
            'available': is_available
        })
    
    context = {
        'room': table,  # Keep 'room' for template compatibility
        'images': images,
        'availability_data': availability_data,
    }
    return render(request, 'rooms/room_detail.html', context)

@login_required
def book_room(request, room_id):
    table = get_object_or_404(Table, id=room_id, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, table=table)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.table = table
            reservation.save()
            
            messages.success(request, f'Table reserved successfully! Reservation reference: {reservation.reservation_reference}')
            return redirect('rooms:booking_detail', booking_id=reservation.id)
    else:
        # Pre-fill form with search parameters if available
        initial_data = {}
        if request.GET.get('reservation_date'):
            initial_data['reservation_date'] = request.GET.get('reservation_date')
        if request.GET.get('reservation_time'):
            initial_data['reservation_time'] = request.GET.get('reservation_time')
        if request.GET.get('party_size'):
            initial_data['party_size'] = request.GET.get('party_size')
        
        form = BookingForm(initial=initial_data, table=table)
    
    context = {
        'room': table,  # Keep 'room' for template compatibility
        'form': form,
    }
    return render(request, 'rooms/book_room.html', context)

@login_required
def booking_detail(request, booking_id):
    reservation = get_object_or_404(Reservation, id=booking_id, user=request.user)
    context = {
        'booking': reservation  # Keep 'booking' for template compatibility
    }
    return render(request, 'rooms/booking_detail.html', context)

@login_required
def my_bookings(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'rooms/my_bookings.html', {'page_obj': page_obj})

@login_required
def cancel_booking(request, booking_id):
    reservation = get_object_or_404(Reservation, id=booking_id, user=request.user)
    
    if reservation.status in ['pending', 'confirmed'] and reservation.reservation_date > date.today():
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reservation cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this reservation.')
    
    return redirect('rooms:my_bookings')

def check_availability(request):
    """AJAX endpoint to check table availability"""
    if request.method == 'GET':
        table_id = request.GET.get('room_id')  # Keep 'room_id' for compatibility
        reservation_date = request.GET.get('reservation_date')
        reservation_time = request.GET.get('reservation_time')
        
        if table_id and reservation_date and reservation_time:
            try:
                table = Table.objects.get(id=table_id)
                res_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
                res_time = datetime.strptime(reservation_time, '%H:%M').time()
                
                is_available = table.is_available(res_date, res_time)
                
                return JsonResponse({
                    'available': is_available,
                    'message': 'Table is available' if is_available else 'Table is not available for selected date and time'
                })
            except (Table.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Invalid data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)