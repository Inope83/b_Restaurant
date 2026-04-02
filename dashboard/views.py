from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from rooms.models import Table, Reservation, TableType
from accounts.models import User

def home(request):
    """Public home page"""
    table_types = TableType.objects.all()[:3]  # Show first 3 table types
    featured_tables = Table.objects.filter(is_active=True)[:6]  # Show 6 featured tables
    
    context = {
        'table_types': table_types,
        'featured_tables': featured_tables,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    if user.role == 'admin':
        return admin_dashboard(request)
    else:
        return customer_dashboard(request)

@login_required
def customer_dashboard(request):
    """Customer dashboard with reservation history and profile info"""
    user = request.user
    
    # Get user's reservations
    recent_reservations = Reservation.objects.filter(user=user).order_by('-created_at')[:5]
    upcoming_reservations = Reservation.objects.filter(
        user=user,
        reservation_date__gte=timezone.now().date(),
        status__in=['confirmed', 'pending']
    ).order_by('reservation_date')
    
    # Calculate user statistics
    total_reservations = Reservation.objects.filter(user=user).count()
    total_spent = Reservation.objects.filter(
        user=user,
        status__in=['confirmed', 'seated', 'completed']
    ).aggregate(total=Sum('final_amount'))['total'] or 0
    
    context = {
        'user': user,
        'recent_reservations': recent_reservations,
        'upcoming_reservations': upcoming_reservations,
        'total_reservations': total_reservations,
        'total_spent': total_spent,
    }
    return render(request, 'dashboard/customer_dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics and management overview"""
    if request.user.role != 'admin':
        return redirect('dashboard:dashboard')
    
    # Date range for statistics (last 30 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Basic statistics
    total_tables = Table.objects.count()
    available_tables = Table.objects.filter(status='available').count()
    total_reservations = Reservation.objects.count()
    total_customers = User.objects.filter(role='customer').count()
    
    # Revenue statistics
    total_revenue = Reservation.objects.filter(
        status__in=['confirmed', 'seated', 'completed']
    ).aggregate(total=Sum('final_amount'))['total'] or 0
    
    monthly_revenue = Reservation.objects.filter(
        created_at__date__gte=start_date,
        status__in=['confirmed', 'seated', 'completed']
    ).aggregate(total=Sum('final_amount'))['total'] or 0
    
    # Recent reservations
    recent_reservations = Reservation.objects.order_by('-created_at')[:10]
    
    # Table occupancy
    occupied_tables = Table.objects.filter(status='occupied').count()
    occupancy_rate = (occupied_tables / total_tables * 100) if total_tables > 0 else 0
    
    # Most reserved table types
    popular_table_types = TableType.objects.annotate(
        reservation_count=Count('tables__reservations')
    ).order_by('-reservation_count')[:5]
    
    # Reservation status distribution
    reservation_stats = Reservation.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Customer advantage level distribution
    customer_levels = User.objects.filter(role='customer').values('advantage_level').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_tables': total_tables,
        'available_tables': available_tables,
        'total_reservations': total_reservations,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'recent_reservations': recent_reservations,
        'occupancy_rate': round(occupancy_rate, 1),
        'popular_table_types': popular_table_types,
        'reservation_stats': reservation_stats,
        'customer_levels': customer_levels,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)