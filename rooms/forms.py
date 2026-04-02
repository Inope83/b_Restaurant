from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Table, Reservation, TableType, TableImage

class RoomSearchForm(forms.Form):
    reservation_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': date.today().strftime('%Y-%m-%d')
        })
    )
    reservation_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    party_size = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '20'
        })
    )
    table_type = forms.ModelChoiceField(
        queryset=TableType.objects.all(),
        required=False,
        empty_label="Any Table Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        
        if reservation_date:
            if reservation_date < date.today():
                raise ValidationError("Reservation date cannot be in the past.")
        
        return cleaned_data

class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size', 'special_requests']
        widgets = {
            'reservation_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().strftime('%Y-%m-%d')
            }),
            'reservation_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'party_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests, dietary restrictions, or preferences...'
            })
        }
    
    def __init__(self, *args, table=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = table
        if table:
            self.fields['party_size'].widget.attrs['max'] = table.table_type.max_capacity
    
    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        reservation_time = cleaned_data.get('reservation_time')
        party_size = cleaned_data.get('party_size')
        
        if reservation_date:
            if reservation_date < date.today():
                raise ValidationError("Reservation date cannot be in the past.")
            
            if self.table and not self.table.is_available(reservation_date, reservation_time):
                raise ValidationError("Table is not available for the selected date and time.")
        
        if party_size and self.table and party_size > self.table.table_type.max_capacity:
            raise ValidationError(f"Maximum capacity for this table is {self.table.table_type.max_capacity} people.")
        
        return cleaned_data

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'table_type', 'location', 'status', 'description', 'reservation_fee', 'is_active']
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'form-control'}),
            'table_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reservation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TableImageForm(forms.ModelForm):
    class Meta:
        model = TableImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }