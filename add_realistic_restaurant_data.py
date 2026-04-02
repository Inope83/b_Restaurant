#!/usr/bin/env python
"""
Script to add realistic restaurant table data to the database
Run this with: python manage.py shell < add_realistic_restaurant_data.py
"""

from rooms.models import TableType, Table

# Clear existing data
print("Clearing existing data...")
Table.objects.all().delete()
TableType.objects.all().delete()

# Create realistic Table Types
table_types_data = [
    {
        'name': 'Intimate Booth',
        'description': 'Cozy booth seating perfect for romantic dinners and intimate conversations',
        'base_price': 35.00,
        'max_capacity': 2,
        'features': 'Private booth, Soft lighting, Cushioned seating, Romantic ambiance'
    },
    {
        'name': 'Standard Dining Table',
        'description': 'Classic four-person table ideal for family meals and casual dining',
        'base_price': 25.00,
        'max_capacity': 4,
        'features': 'Comfortable chairs, Table service, Central location, Perfect for families'
    },
    {
        'name': 'Large Family Table',
        'description': 'Spacious table designed for larger groups and family gatherings',
        'base_price': 45.00,
        'max_capacity': 8,
        'features': 'Extra spacious, High chairs available, Group-friendly, Celebration setup'
    },
    {
        'name': 'Chef\'s Counter',
        'description': 'Premium counter seating with kitchen view and chef interaction',
        'base_price': 60.00,
        'max_capacity': 6,
        'features': 'Kitchen view, Chef interaction, Premium experience, Wine pairing available'
    },
    {
        'name': 'Outdoor Patio Table',
        'description': 'Al fresco dining with garden views and fresh air',
        'base_price': 30.00,
        'max_capacity': 4,
        'features': 'Garden view, Fresh air, Weather protection, Outdoor heaters'
    },
    {
        'name': 'Private Dining Room',
        'description': 'Exclusive private room for special occasions and business meetings',
        'base_price': 100.00,
        'max_capacity': 12,
        'features': 'Complete privacy, Dedicated server, AV equipment, Custom menu options'
    }
]

print("Creating realistic table types...")
for data in table_types_data:
    table_type, created = TableType.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        print(f"✓ Created table type: {table_type.name}")
    else:
        print(f"- Table type already exists: {table_type.name}")

# Create realistic Tables with proper restaurant layout
tables_data = [
    # Main Dining Room - Standard Tables
    {'table_number': '101', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Window-side table with street view'},
    {'table_number': '102', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Central table in main dining area'},
    {'table_number': '103', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Corner table with cozy atmosphere'},
    {'table_number': '104', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Table near the fireplace'},
    {'table_number': '105', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Quiet table away from kitchen'},
    {'table_number': '106', 'table_type': 'Standard Dining Table', 'location': 'Main Dining Room', 'reservation_fee': 25.00, 'description': 'Table with art gallery view'},
    
    # Intimate Booths
    {'table_number': 'B01', 'table_type': 'Intimate Booth', 'location': 'Booth Section', 'reservation_fee': 35.00, 'description': 'Romantic booth with dimmed lighting'},
    {'table_number': 'B02', 'table_type': 'Intimate Booth', 'location': 'Booth Section', 'reservation_fee': 35.00, 'description': 'Private booth perfect for date nights'},
    {'table_number': 'B03', 'table_type': 'Intimate Booth', 'location': 'Booth Section', 'reservation_fee': 35.00, 'description': 'Secluded booth with wine display view'},
    {'table_number': 'B04', 'table_type': 'Intimate Booth', 'location': 'Booth Section', 'reservation_fee': 35.00, 'description': 'Corner booth with maximum privacy'},
    
    # Family Tables
    {'table_number': 'F01', 'table_type': 'Large Family Table', 'location': 'Family Section', 'reservation_fee': 45.00, 'description': 'Large round table perfect for celebrations'},
    {'table_number': 'F02', 'table_type': 'Large Family Table', 'location': 'Family Section', 'reservation_fee': 45.00, 'description': 'Rectangular table ideal for large groups'},
    {'table_number': 'F03', 'table_type': 'Large Family Table', 'location': 'Family Section', 'reservation_fee': 45.00, 'description': 'Family table with high chair access'},
    
    # Chef's Counter
    {'table_number': 'CC1', 'table_type': 'Chef\'s Counter', 'location': 'Kitchen Counter', 'reservation_fee': 60.00, 'description': 'Front row seats to culinary action'},
    {'table_number': 'CC2', 'table_type': 'Chef\'s Counter', 'location': 'Kitchen Counter', 'reservation_fee': 60.00, 'description': 'Premium counter with chef interaction'},
    
    # Outdoor Patio
    {'table_number': 'P01', 'table_type': 'Outdoor Patio Table', 'location': 'Garden Patio', 'reservation_fee': 30.00, 'description': 'Garden view table with herb garden nearby'},
    {'table_number': 'P02', 'table_type': 'Outdoor Patio Table', 'location': 'Garden Patio', 'reservation_fee': 30.00, 'description': 'Patio table under the pergola'},
    {'table_number': 'P03', 'table_type': 'Outdoor Patio Table', 'location': 'Garden Patio', 'reservation_fee': 30.00, 'description': 'Fountain-side table with water sounds'},
    {'table_number': 'P04', 'table_type': 'Outdoor Patio Table', 'location': 'Rooftop Terrace', 'reservation_fee': 35.00, 'description': 'Rooftop table with city skyline view'},
    {'table_number': 'P05', 'table_type': 'Outdoor Patio Table', 'location': 'Rooftop Terrace', 'reservation_fee': 35.00, 'description': 'Terrace table perfect for sunset dining'},
    {'table_number': 'P06', 'table_type': 'Outdoor Patio Table', 'location': 'Rooftop Terrace', 'reservation_fee': 35.00, 'description': 'Meza iha terrasu ho esperiénsia han iha li\'ur.'},
    
    # Private Dining
    {'table_number': 'PDR1', 'table_type': 'Private Dining Room', 'location': 'Private Dining Room', 'reservation_fee': 100.00, 'description': 'Executive boardroom-style dining for business meetings'},
    {'table_number': 'PDR2', 'table_type': 'Private Dining Room', 'location': 'Wine Cellar Room', 'reservation_fee': 120.00, 'description': 'Intimate wine cellar dining with sommelier service'},
    
    # Bar Area Tables
    {'table_number': 'BAR1', 'table_type': 'Standard Dining Table', 'location': 'Bar Area', 'reservation_fee': 20.00, 'description': 'High-top table near the bar with cocktail service'},
    {'table_number': 'BAR2', 'table_type': 'Standard Dining Table', 'location': 'Bar Area', 'reservation_fee': 20.00, 'description': 'Bar-side table perfect for drinks and appetizers'},
    {'table_number': 'BAR3', 'table_type': 'Intimate Booth', 'location': 'Bar Area', 'reservation_fee': 30.00, 'description': 'Cozy booth in the bar area with craft cocktail focus'},
]

print("\nCreating realistic restaurant tables...")
for data in tables_data:
    try:
        table_type = TableType.objects.get(name=data['table_type'])
        table, created = Table.objects.get_or_create(
            table_number=data['table_number'],
            defaults={
                'table_type': table_type,
                'location': data['location'],
                'reservation_fee': data['reservation_fee'],
                'status': 'available',
                'is_active': True,
                'description': data['description']
            }
        )
        if created:
            print(f"✓ Created table: {table.table_number} - {table.description}")
        else:
            print(f"- Table already exists: {table.table_number}")
    except TableType.DoesNotExist:
        print(f"✗ Error: Table type '{data['table_type']}' not found")

print(f"\n🍽️  Realistic restaurant data creation completed!")
print(f"📊 Total Table Types: {TableType.objects.count()}")
print(f"🪑 Total Tables: {Table.objects.count()}")
print("\n🎯 Your restaurant now features:")
print("   • Main Dining Room with window and fireplace tables")
print("   • Romantic booth section for intimate dining")
print("   • Family section for large groups and celebrations")
print("   • Chef's counter for culinary enthusiasts")
print("   • Outdoor patio and rooftop terrace")
print("   • Private dining rooms for special occasions")
print("   • Bar area for casual dining and cocktails")
print("\n🌐 Visit your restaurant:")
print("   • Home: http://127.0.0.1:8000/")
print("   • Tables: http://127.0.0.1:8000/tables/")
print("   • Admin: http://127.0.0.1:8000/admin/")
print("\n✨ Ready to serve customers!")