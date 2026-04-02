# 🍽️ b_Restaurant — Restaurant Table Reservation System

A full-featured restaurant table reservation and management system built with **Django 6.0.3**.  
Customers can browse tables, make reservations, and track loyalty rewards. Admins manage everything from a central dashboard.

---

## 📋 Table of Contents

1. [Tech Stack](#-tech-stack)
2. [Project Structure](#-project-structure)
3. [Setup Guide — Windows](#-setup-guide--windows)
4. [Setup Guide — Linux](#-setup-guide--linux)
5. [How the System Works](#-how-the-system-works)
   - [Registration & Login Flow](#1-registration--login-flow)
   - [Browsing & Searching Tables](#2-browsing--searching-tables)
   - [Making a Reservation](#3-making-a-reservation)
   - [Pricing & Discount Calculation](#4-pricing--discount-calculation)
   - [Loyalty / Advantage Level System](#5-loyalty--advantage-level-system)
   - [Payment Flow](#6-payment-flow)
   - [Cancellation Flow](#7-cancellation-flow)
   - [Customer Dashboard](#8-customer-dashboard)
   - [Admin Dashboard](#9-admin-dashboard)
6. [Database Models](#-database-models)
7. [URL Routes](#-url-routes)
8. [Dining Areas & Tables](#-dining-areas--tables)
9. [Default Credentials](#-default-credentials)
10. [Environment Notes](#-environment-notes)

---

## 🛠️ Tech Stack

| Component | Detail |
|---|---|
| Framework | Django==6.0.3 |
| Language | Python 3.x |
| Database | SQLite (`db.sqlite3`) |
| Image Handling | Pillow 12.2.0 |
| Auth | Custom User Model (`accounts.User`) |
| Frontend | Django Templates + Bootstrap |
| Availability Check | AJAX (JSON response) |

---

## 🗂️ Project Structure

```
b_Restaurant/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── add_realistic_restaurant_data.py   # Seed script for table data
├── quick_start.bat                    # Windows one-click launcher
│
├── restaurant_management/             # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                          # App: Auth & user management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── rooms/                             # App: Tables & reservations
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── dashboard/                         # App: Dashboard & home
│   ├── views.py
│   └── urls.py
│
├── templates/                         # HTML templates
├── static/                            # CSS, JS, assets
└── media/                             # User-uploaded files
```

---

## 🪟 Setup Guide — Windows

### Requirements
- Python 3.14+ → https://www.python.org/downloads/
- pip (included with Python)
- Git (optional) → https://git-scm.com/

### Step 1 — Clone or Extract Project
```bat
:: If using Git:
git clone <repo-url>
cd b_Restaurant

:: Or extract ZIP and open Command Prompt in the project folder
```

### Step 2 — Create Virtual Environment
```bat
python -m venv venv
venv\Scripts\activate
```

> You should see `(venv)` at the start of your terminal line.

### Step 3 — Install Dependencies
```bat
pip install -r requirements.txt
```

### Step 4 — Run Migrations
```bat
python manage.py makemigrations accounts rooms dashboard
python manage.py migrate
```

### Step 5 — Create Admin User
```bat
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### Step 6 — Load Sample Restaurant Data
```bat
python manage.py shell < add_realistic_restaurant_data.py
```

This creates 26 tables across 9 dining areas automatically.

### Step 7 — Start the Server
```bat
python manage.py runserver
```

### ⚡ One-Click Option (Windows Only)
If you don't want to run steps manually, just double-click:
```
quick_start.bat
```

### ✅ Access the App
| URL | Description |
|---|---|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/tables/ | Browse tables |
| http://127.0.0.1:8000/dashboard/ | Dashboard |
| http://127.0.0.1:8000/admin/ | Admin panel |

### 🔁 Next Time (Restart Server)
```bat
venv\Scripts\activate
python manage.py runserver
```

---

## 🐧 Setup Guide — Linux

### Requirements
```bash
# Check Python version (need 3.10+)
python3 --version

# Install Python & pip if not installed (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# For Fedora/RHEL:
sudo dnf install python3 python3-pip git -y

# For Arch:
sudo pacman -S python python-pip git
```

### Step 1 — Clone or Extract Project
```bash
# If using Git:
git clone <repo-url>
cd b_Restaurant

# Or extract ZIP:
unzip b_Restaurant.zip
cd b_Restaurant
```

### Step 2 — Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

> You should see `(venv)` at the start of your terminal line.

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

> If Pillow fails to install, install the required system library first:
> ```bash
> # Ubuntu/Debian:
> sudo apt install libjpeg-dev zlib1g-dev -y
> 
> # Fedora:
> sudo dnf install libjpeg-devel zlib-devel -y
> 
> # Then retry:
> pip install -r requirements.txt
> ```

### Step 4 — Run Migrations
```bash
python manage.py makemigrations accounts rooms dashboard
python manage.py migrate
```

### Step 5 — Create Admin User
```bash
python manage.py createsuperuser
```

### Step 6 — Load Sample Restaurant Data
```bash
python manage.py shell < add_realistic_restaurant_data.py
```

### Step 7 — Start the Server
```bash
python manage.py runserver
```

### ⚡ One-Command Setup (Linux Shortcut)
You can run all steps in one go after activating the virtual environment:
```bash
source venv/bin/activate && \
pip install -r requirements.txt && \
python manage.py makemigrations accounts rooms dashboard && \
python manage.py migrate && \
python manage.py shell < add_realistic_restaurant_data.py && \
python manage.py runserver
```

### ✅ Access the App
| URL | Description |
|---|---|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/tables/ | Browse tables |
| http://127.0.0.1:8000/dashboard/ | Dashboard |
| http://127.0.0.1:8000/admin/ | Admin panel |

### 🔁 Next Time (Restart Server)
```bash
source venv/bin/activate
python manage.py runserver
```

### 🌐 Allow Access from Other Devices on the Same Network (Linux)
```bash
python manage.py runserver 0.0.0.0:8000
```
Then access from another device using your machine's local IP, e.g. `http://192.168.1.x:8000/`

---

## ⚙️ How the System Works

### 1. Registration & Login Flow

```
User visits /accounts/register/
        │
        ▼
Fills in: username, email, first name, last name,
          phone (optional), address (optional), password
        │
        ▼
System creates User with:
  - role = 'customer'  (default)
  - advantage_level = 'bronze'  (default)
  - total_bookings = 0
        │
        ▼
Redirected to /accounts/login/
        │
        ▼
After login → redirected to home page (/)
```

> **Note:** If the user is a superuser or staff, the system **automatically sets role = 'admin'** on every save.

**Profile Update** (`/accounts/profile/`):
- Customer can update: first name, last name, email, phone, address, profile picture
- Profile picture is uploaded to `media/profiles/`

---

### 2. Browsing & Searching Tables

```
User visits /tables/
        │
        ▼
Sees all active tables (is_active=True), paginated 6 per page
        │
        ▼
Can filter by:
  ├── Table Type      → e.g. Intimate Booth, Chef's Counter
  ├── Party Size      → filters tables where max_capacity >= party_size
  ├── Date            → must be today or future
  └── Time            → checks real-time availability
        │
        ▼
For each table: system calls table.is_available(date, time)
  └── Checks: no overlapping confirmed/seated reservations
              AND table.status == 'available'
        │
        ▼
User clicks a table → /tables/<id>/
  └── Shows: table details, images, features
             30-day availability calendar (checks 7PM dinner slot each day)
```

**AJAX Availability Check** (`/tables/check-availability/`):
- Called live from the browser with `table_id`, `date`, `time`
- Returns JSON: `{ "available": true/false, "message": "..." }`
- No page reload needed

---

### 3. Making a Reservation

```
User clicks "Reserve" on a table → /tables/<id>/reserve/
        │  (login required — redirects to login if not authenticated)
        ▼
Fills in BookingForm:
  - reservation_date  (today or future only)
  - reservation_time
  - party_size        (max = table's max_capacity)
  - special_requests  (optional free text)
        │
        ▼
Form validation:
  ├── Date must not be in the past
  ├── Party size must not exceed table capacity
  └── table.is_available(date, time) must return True
        │
        ▼
Reservation object created:
  - user = logged-in user
  - table = selected table
  - status = 'pending'
  - payment_status = 'pending'
  - reservation_reference = auto UUID (e.g. "A1B2C3D4")
  - end_time = reservation_time + 2 hours (auto-calculated)
  - Pricing calculated automatically (see section 4)
        │
        ▼
Redirected to /tables/reservation/<id>/
  └── Shows: reference code, table, date/time, party size,
             amounts, status, special requests
```

---

### 4. Pricing & Discount Calculation

Every time a `Reservation` is saved, the system automatically computes:

```
base_amount       = table.reservation_fee
discount_%        = user.get_discount_percentage()  (based on advantage_level)
discount_amount   = base_amount × discount_%
final_amount      = base_amount − discount_amount
total_amount      = base_amount  (original, before discount)
```

**Example:**
```
Table CC1 (Chef's Counter) → reservation_fee = $60
User is Gold level          → discount = 10%
discount_amount             = $60 × 10% = $6
final_amount                = $60 − $6  = $54
```

---

### 5. Loyalty / Advantage Level System

Every time a reservation is **confirmed**, the system:
1. Increments `user.total_bookings += 1`
2. Calls `user.update_advantage_level()` which re-evaluates the tier

```
total_bookings >= 20  →  💎 Platinum  (15% discount)
total_bookings >= 10  →  🥇 Gold      (10% discount)
total_bookings >=  5  →  🥈 Silver    ( 5% discount)
total_bookings <   5  →  🥉 Bronze    ( 0% discount)
```

The discount is applied automatically on the **next** reservation.

---

### 6. Payment Flow

```
After reservation is created (status: pending, payment_status: pending)
        │
        ▼
Admin records payment via Admin Panel → /admin/rooms/payment/add/
        │
        ▼
Payment fields:
  - reservation   → links to the reservation
  - amount
  - payment_method: cash / credit_card / debit_card / bank_transfer / online
  - transaction_id (optional)
  - notes (optional)
        │
        ▼
Admin updates reservation payment_status:
  pending → partial → paid
        │
        ▼
Admin updates reservation status:
  pending → confirmed → seated → completed
```

---

### 7. Cancellation Flow

```
Customer visits /tables/my-reservations/
        │
        ▼
Sees all reservations (paginated, 10 per page)
        │
        ▼
Clicks "Cancel" on a reservation
        │
        ▼
System checks:
  ├── status must be 'pending' or 'confirmed'
  └── reservation_date must be in the future
        │
     ┌──┴──┐
    Yes    No
     │      └── Error: "Cannot cancel this reservation"
     ▼
status → 'cancelled'
Redirected back to /tables/my-reservations/
```

---

### 8. Customer Dashboard

Accessible at `/dashboard/` for users with `role = 'customer'`.

| Section | Description |
|---|---|
| Recent Reservations | Last 5 reservations (any status) |
| Upcoming Reservations | Future reservations with status `confirmed` or `pending` |
| Total Reservations | Lifetime count |
| Total Spent | Sum of `final_amount` for completed/confirmed reservations |
| Profile Info | Name, advantage level, discount % |

---

### 9. Admin Dashboard

Accessible at `/dashboard/` for users with `role = 'admin'`.

| Section | What it shows |
|---|---|
| Total Tables | Count of all tables |
| Available Tables | Tables with status = `available` |
| Total Customers | Users with role = `customer` |
| Total Reservations | All-time count |
| Total Revenue | Sum of `final_amount` (confirmed/seated/completed) |
| Monthly Revenue | Revenue in last 30 days |
| Occupancy Rate | % of tables currently occupied |
| Recent Reservations | Last 10 reservations across all users |
| Popular Table Types | Ranked by reservation count |
| Reservation Status | Breakdown: pending/confirmed/seated/completed/cancelled |
| Customer Levels | Breakdown: bronze/silver/gold/platinum |

---

## 🗃️ Database Models

### `accounts.User`
| Field | Type | Notes |
|---|---|---|
| `username`, `email`, `password` | — | Standard Django fields |
| `role` | CharField | `admin` or `customer` (default: `customer`) |
| `phone` | CharField | Optional |
| `address` | TextField | Optional |
| `advantage_level` | CharField | `bronze` / `silver` / `gold` / `platinum` |
| `total_bookings` | PositiveIntegerField | Auto-incremented on confirmed reservation |
| `profile_picture` | ImageField | Uploaded to `media/profiles/` |
| `created_at` / `updated_at` | DateTimeField | Auto timestamps |

### `rooms.TableType`
| Field | Notes |
|---|---|
| `name` | Unique, e.g. "Intimate Booth" |
| `description` | Long description |
| `base_price` | Reference price |
| `max_capacity` | Max guests for this type |
| `features` | Comma-separated, e.g. "Kitchen view, Wine pairing" |

### `rooms.Table`
| Field | Notes |
|---|---|
| `table_number` | Unique, e.g. "B01", "CC1" |
| `table_type` | FK → TableType |
| `location` | e.g. "Garden Patio" |
| `status` | `available` / `occupied` / `reserved` / `maintenance` |
| `reservation_fee` | Actual fee charged |
| `is_active` | False = hidden from customers |
| `description` | e.g. "Window-side table with street view" |

### `rooms.TableImage`
| Field | Notes |
|---|---|
| `table` | FK → Table |
| `image` | Uploaded to `media/table_images/` |
| `caption` | Optional label |
| `is_primary` | Primary image shown first |

### `rooms.Reservation`
| Field | Notes |
|---|---|
| `reservation_reference` | Auto 8-char UUID (e.g. `A1B2C3D4`) |
| `user` | FK → User |
| `table` | FK → Table |
| `reservation_date` / `reservation_time` | When |
| `end_time` | Auto = start + 2 hours |
| `party_size` | Number of guests |
| `status` | `pending` → `confirmed` → `seated` → `completed` |
| `payment_status` | `pending` → `partial` → `paid` |
| `total_amount` / `discount_amount` / `final_amount` | Pricing breakdown |
| `special_requests` | Dietary needs, celebrations, etc. |

### `rooms.Payment`
| Field | Notes |
|---|---|
| `reservation` | FK → Reservation |
| `amount` | Amount paid |
| `payment_method` | `cash` / `credit_card` / `debit_card` / `bank_transfer` / `online` |
| `transaction_id` | Optional external reference |

---

## 🌐 URL Routes

| URL | View | Access |
|---|---|---|
| `/` | Home — featured tables & types | Public |
| `/dashboard/` | Customer or Admin dashboard | Login required |
| `/accounts/register/` | Register | Public |
| `/accounts/login/` | Login | Public |
| `/accounts/logout/` | Logout | Login required |
| `/accounts/profile/` | View & edit profile | Login required |
| `/tables/` | Browse & search all tables | Public |
| `/tables/<id>/` | Table detail + 30-day calendar | Public |
| `/tables/<id>/reserve/` | Make a reservation | Login required |
| `/tables/reservation/<id>/` | Reservation detail | Login required |
| `/tables/my-reservations/` | My booking history | Login required |
| `/tables/cancel-reservation/<id>/` | Cancel a reservation | Login required |
| `/tables/check-availability/` | AJAX availability check (JSON) | Public |
| `/admin/` | Django admin panel | Admin only |

---

## 🪑 Dining Areas & Tables

| Area | Tables | Capacity | Fee |
|---|---|---|---|
| Main Dining Room | 101 – 106 | 4 pax | $25 |
| Booth Section | B01 – B04 | 2 pax | $35 |
| Family Section | F01 – F03 | 8 pax | $45 |
| Chef's Counter | CC1 – CC2 | 6 pax | $60 |
| Garden Patio | P01 – P03 | 4 pax | $30 |
| Rooftop Terrace | P04 – P06 | 4 pax | $35 |
| Private Dining Room | PDR1 | 12 pax | $100 |
| Wine Cellar Room | PDR2 | 12 pax | $120 |
| Bar Area | BAR1 – BAR3 | 2–4 pax | $20–30 |

**Total: 26 tables across 9 areas**

---

## 🔑 Default Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |

> ⚠️ Change the default password and `SECRET_KEY` in `settings.py` before deploying to production.

---

## ⚙️ Environment Notes

| Setting | Value | Notes |
|---|---|---|
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `localhost`, `127.0.0.1` | Add your domain in production |
| `DATABASE` | SQLite | Switch to PostgreSQL for production |
| `MEDIA_URL` | `/media/` | User-uploaded files served locally |
| `EMAIL_BACKEND` | Console output | No SMTP setup needed for development |
| `SECRET_KEY` | Placeholder | **Must be changed before going live** |

---

## 📄 Requirements

```
asgiref==3.11.1
Django==6.0.3
pillow==12.2.0
sqlparse==0.5.5

```
