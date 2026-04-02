from django.contrib import admin
from .models import TableType, Table, TableImage, Reservation, Payment

@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'max_capacity')
    search_fields = ('name',)

class TableImageInline(admin.TabularInline):
    model = TableImage
    extra = 1

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'table_type', 'location', 'status', 'reservation_fee', 'is_active')
    list_filter = ('table_type', 'location', 'status', 'is_active')
    search_fields = ('table_number', 'table_type__name')
    inlines = [TableImageInline]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_reference', 'user', 'table', 'reservation_date', 'reservation_time', 'party_size', 'status', 'payment_status', 'final_amount')
    list_filter = ('status', 'payment_status', 'reservation_date', 'created_at')
    search_fields = ('reservation_reference', 'user__username', 'table__table_number')
    readonly_fields = ('reservation_reference', 'total_amount', 'discount_amount', 'final_amount', 'end_time')
    date_hierarchy = 'reservation_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('reservation__reservation_reference', 'transaction_id')