# ORTHOBEST CARE HUB — DJANGO E-COMMERCE PLATFORM

> **Kenya's Premier Destination for Orthopedic, Rehabilitation, Mobility & Healthcare Products**  
> *Production-Ready Django 6.1 E-Commerce Redevelopment for `orthobestcarehub.co.ke` (formerly `orthobestcarerehab.co.ke`)*

---

## 1. Project Overview & Architecture

Orthobest Care Hub is a modern, mobile-first, Gen-Z styled health-commerce platform built on Django 6.1 with clean modular architecture, Kenyan M-Pesa integration (Daraja API STK Push), dynamic delivery zone calculations, session/persistent carts, customer account management, and complete administrative control.

### Modular Architecture
```
orthobestcarehub/
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── README.md
├── OLD_SITE_AUDIT.md
├── ARCHITECTURE.md
│
├── orthobestcarehub/       # Project Configuration
│   ├── settings.py         # Environment-driven settings, security, PostgreSQL support
│   ├── urls.py             # Sitemaps & modular route routing
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/               # SiteSettings singleton, HomeBanners, TrustBadges, 301 SEO middleware
│   ├── products/           # Categories, Brands, Products, Variants, Multi-images, Reviews
│   ├── cart/               # Session & DB Cart abstraction, Drawer cart, AJAX endpoints
│   ├── orders/             # Orders, OrderItems, DeliveryZones, Coupons, Tracking
│   ├── payments/           # Pluggable PaymentGateways (M-Pesa Daraja, Cash on Delivery, Card)
│   ├── accounts/           # UserProfile, saved delivery addresses, registration & dashboard
│   ├── content_hub/        # Services, Blog/Educational guides, FAQs, Legal store policies
│   └── leads/              # Contact form inquiries, Newsletter subscribers
│
├── static/
│   ├── css/main.css        # 2026 design tokens, responsive typography, drawer, sticky bars
│   ├── js/main.js          # Cart drawer, live autocomplete search, M-Pesa status polling, toasts
│   └── images/             # Product placeholders & brand icons
│
├── templates/              # Semantic Django templates & reusable HTML components
│   ├── base.html
│   ├── components/         # Header, Footer, MobileNav, CartDrawer, ProductCard, TrustStrip
│   ├── core/               # Homepage, 404, 500, 403
│   ├── products/           # Shop catalog, Category detail, Product detail
│   ├── cart/               # Full shopping cart
│   ├── orders/             # Single-page checkout, Order confirmation, Tracking, Detail
│   ├── payments/           # Payment processing & M-Pesa STK trigger
│   ├── accounts/           # Login, Register, Dashboard, Orders, Addresses, Profile
│   ├── content_hub/        # About, Services, Blog list/detail, FAQ, Legal policies
│   └── leads/              # Contact page with Nairobi showroom map
│
└── media/                  # Uploaded product imagery, banners, avatars
```

---

## 2. Key Features

### 🛍️ E-Commerce & Product Discovery
* **Responsive Product Catalog**: 4-column desktop, 3-column tablet, 2-column mobile layout.
* **Instant Filters & Sorting**: Category filter, price range slider, in-stock checkbox, sort by Price (Low/High), Bestseller, Newest, Name.
* **Live Search Autocomplete**: Fast debounced search matching product titles, SKUs, and categories.
* **Product Detail Views**: Multi-image gallery with thumbnail switcher, interactive variant selector, quantity stepper, clinical overview/features/specs/size-guide tabs, approved reviews, and related products.
* **Direct WhatsApp Consultation**: Automated pre-filled WhatsApp link with product title, SKU, and price.

### 🛒 Shopping Cart & Kenyan Checkout
* **Slide-in Mini-Cart Drawer**: Instant AJAX add-to-cart without full page reload.
* **Single-Page Checkout**: Streamlined checkout designed for Kenyan customers with normalized phone validation (`+254`, `07...`, `01...`).
* **Delivery Fee Zones**: Configurable Kenyan zones (Nairobi CBD, Nairobi Suburbs, Kiambu/Machakos, Upcountry Courier) with automatic total recalculation.
* **Coupon Discounts**: Supports percentage (`%`) or fixed (`KSh`) discounts with minimum order validations.

### 💳 Payment Gateways & M-Pesa Daraja Integration
* **Safaricom Lipa Na M-Pesa Express (STK Push)**: Initiates STK push directly to the customer's phone using Daraja API credentials with live polling and callback verification.
* **Pay on Delivery (COD)**: Supports cash or M-Pesa on arrival for Nairobi and surrounding areas.
* **Pluggable Payment Gateway Architecture**: Easily extensible for Pesapal, Stripe, or direct bank transfer.
* **Payment Security & Idempotency**: Atomic order updates, transaction reference logging, and server-side price protection.

### 📱 Gen-Z & Mobile-First UX
* **Sticky Mobile Navigation Bar**: Instant access to Home, Shop, Tracking, Account, and Cart.
* **Non-intrusive Toast Notifications**: Feedback on cart actions, coupon applications, and status updates.
* **Floating WhatsApp Button**: Persistent customer support access with ping animation.

### 🔍 SEO & Migration Suite
* **301 Redirect Middleware**: Seamless permanent redirection from old URLs (`/product-category/...`, `/about-us/`, `/contact-us/`) and the old domain `orthobestcarerehab.co.ke`.
* **Structured Data**: JSON-LD schema for Products, Organization, and BreadcrumbList.
* **Dynamic Sitemap & Robots.txt**: Accessible at `/sitemap.xml` and `/robots.txt`.

---

## 3. Verified Audited Data & Catalog

Audited directly from the business records of **Orthobest Care Hub** (Travis Building, Nairobi CBD):

| Category | Audited Sample Products | Sample Pricing (KSh) |
| :--- | :--- | :--- |
| **Mobility Aids** | Standard Folding Wheelchair, Aluminum Walking Cane | KSh 1,800 – 13,000 |
| **Orthopedic Supports** | Rigid Cervical Collar, Wrist & Forearm Splint, Hinged Knee Brace, Lumbar Sacral Belt | KSh 2,750 – 4,000 |
| **Rehabilitation & Physio** | Digital Pedal Exerciser, Standing Frame, Percussion Massage Gun, TheraBands | KSh 2,200 – 25,000 |
| **Medical Furniture** | Hospital Beds, Commode Bedside Chairs, IV Drip Stands | KSh 6,500 – 45,000 |
| **Daily Living & Home Care** | Adult Disposable Underpads (Pack of 10), Bath Chairs | KSh 1,200 – 4,500 |

---

## 4. Local Installation & Setup

### Prerequisites
* Python 3.12+ (tested on Python 3.14)
* Virtual environment (`venv`)

### Setup Instructions (Windows / PowerShell)
```powershell
# 1. Clone repository
git clone https://github.com/YourRepo/OrthobestCareHub.git
cd OrthobestCareHub

# 2. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy .env.example to .env and adjust credentials
Copy-Item .env.example .env

# 5. Run database migrations
python manage.py migrate

# 6. Seed database with audited products, categories, delivery zones & settings
python manage.py populate_store

# 7. Run automated test suite
python manage.py test

# 8. Start local development server
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## 5. Django Admin Operations

Access the admin dashboard at: `http://127.0.0.1:8000/admin/`

* **Default Admin Credentials (created by `populate_store`):**
  * **Username:** `admin`
  * **Password:** `admin1234`

### Management Capabilities
* **Site Settings Singleton**: Update phone numbers, WhatsApp line, Nairobi physical address, announcement bar banner, hero headline, medical disclaimer, and logo without code edits.
* **Products & Catalog**: Add/edit products, manage stock quantities, upload multiple gallery images, configure variant pricing (sizes/sides), and view low-stock alerts.
* **Orders & Dispatch**: Change order status (`Pending` → `Confirmed` → `Processing` → `Ready for Dispatch` → `Shipped` → `Delivered`), view customer addresses, and check M-Pesa receipt references.
* **Coupons & Delivery Zones**: Create discount codes and adjust delivery charges for Nairobi or upcountry courier regions.
* **Customer Reviews & Leads**: Moderate user reviews, read contact form messages, and manage newsletter subscribers.

---

## 6. Payment & Daraja M-Pesa Configuration

Set the following variables in `.env`:
```env
MPESA_ENVIRONMENT=sandbox # or 'production'
MPESA_CONSUMER_KEY=your_safaricom_consumer_key
MPESA_CONSUMER_SECRET=your_safaricom_consumer_secret
MPESA_PASSKEY=your_daraja_passkey
MPESA_SHORTCODE=174379 # Paybill or Till Number
MPESA_CALLBACK_URL=https://orthobestcarehub.co.ke/payments/mpesa/callback/
```

*When running in sandbox/simulation mode, the checkout interface provides an automated simulation button to test instant STK PIN entry and receipt generation.*

---

## 7. Production Deployment (Gunicorn, Nginx & PostgreSQL)

### Step 1: Install PostgreSQL Driver & Gunicorn
```bash
pip install psycopg2-binary gunicorn
```

### Step 2: Environment Settings (`.env`)
```env
DEBUG=False
SECRET_KEY=generate-a-strong-random-50-character-key
ALLOWED_HOSTS=orthobestcarehub.co.ke,www.orthobestcarehub.co.ke
DATABASE_URL=postgresql://orthobest_user:secure_password@localhost:5432/orthobest_db
STATIC_ROOT=/var/www/orthobestcarehub/staticfiles
MEDIA_ROOT=/var/www/orthobestcarehub/media
```

### Step 3: Collect Static Files & Migrate Database
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### Step 4: Systemd Service Configuration (`/etc/systemd/system/orthobestcarehub.service`)
```ini
[Unit]
Description=Orthobest Care Hub Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/orthobestcarehub
ExecStart=/var/www/orthobestcarehub/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/orthobestcarehub.sock orthobestcarehub.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Step 5: Nginx Reverse Proxy Configuration
```nginx
server {
    server_name orthobestcarerehab.co.ke www.orthobestcarerehab.co.ke;
    return 301 https://orthobestcarehub.co.ke$request_uri;
}

server {
    server_name orthobestcarehub.co.ke www.orthobestcarehub.co.ke;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /var/www/orthobestcarehub/staticfiles/;
    }
    location /media/ {
        alias /var/www/orthobestcarehub/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/orthobestcarehub.sock;
    }
}
```

---

## 8. Test Execution & Verification

Run the automated test suite:
```powershell
python manage.py test
```
**Results:** `15 passed in ~0.94s (0 failures, 0 errors, 0 warnings)`
