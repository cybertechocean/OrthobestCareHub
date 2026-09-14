# 🚀 Orthobest Care Hub — Shared Hosting Deployment Guide

Complete step-by-step production deployment manual for **Orthobest Care Hub** on shared hosting (cPanel with CloudLinux / Phusion Passenger).

---

## 📌 Deployment Specifications

| Parameter | Production Value |
| :--- | :--- |
| **Domain Name** | `orthobestcarehub.co.ke` (and `www.orthobestcarehub.co.ke`) |
| **Document Root** | `/home2/genzcons/orthobestcarehub.co.ke` |
| **Application Root (cPanel)** | `orthobestcarehub.co.ke` |
| **Application Directory** | `/home2/genzcons/orthobestcarehub.co.ke` |
| **Python Virtualenv** | `/home2/genzcons/virtualenv/orthobestcarehub.co.ke/3.12/` |
| **Python Version** | `3.12` (3.12.13) |
| **GitHub Repository** | `https://github.com/cybertechocean/OrthobestCareHub` |
| **Primary Email** | `info@orthobestcarehub.co.ke` |
| **Alternate / Gmail** | `orthobestcarehub@gmail.com` |
| **Database Engine** | MariaDB / MySQL |
| **Database Name** | `genzcons_orthobestcare` (or `orthobestcare`) |
| **Database User** | `genzcons_orthobestuser` (or `orthobestuser`) |
| **WSGI Entry Point** | `passenger_wsgi.py` (`application`) |
| **Static Handling** | WhiteNoise (`CompressedManifestStaticFilesStorage`) |
| **Cache System** | Django DatabaseCache (`orthobest_cache_table`) |

---

## 🛠️ Step 1: Create MariaDB Database & User in cPanel

1. Log in to your **cPanel** dashboard (user: `genzcons`).
2. Navigate to **Databases** → **MySQL® Databases** (or **MariaDB Databases**).
3. Under **Create New Database**:
   - Database Name: enter `orthobestcare` (cPanel will create it as **`genzcons_orthobestcare`**).
   - Click **Create Database**.
4. Under **Add New User**:
   - Username: enter `orthobestuser` (cPanel will create it as **`genzcons_orthobestuser`**).
   - Password: click **Password Generator** (generate a strong 18+ character password, copy it and save it for `.env`).
   - Click **Create User**.
5. Under **Add User To Database**:
   - Select User: `genzcons_orthobestuser`
   - Select Database: `genzcons_orthobestcare`
   - Click **Add**.
   - Check **ALL PRIVILEGES** and click **Make Changes**.

---

## 🐍 Step 2: Configure Python App in cPanel

1. In cPanel, navigate to **Software** → **Setup Python App**.
2. Click **Create Application**.
3. Fill in the exact fields:
   - **Python version**: Select **`3.12`** (3.12.13).
   - **Application root**: `orthobestcarehub.co.ke`
     *(This automatically targets `/home2/genzcons/orthobestcarehub.co.ke`)*
   - **Application URL**: Select `orthobestcarehub.co.ke` from the domain dropdown.
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
4. Click **Create** (at top right).
5. Once created, cPanel will display your virtual environment activation command at the top, which looks like:
   ```bash
   source /home2/genzcons/virtualenv/orthobestcarehub.co.ke/3.12/bin/activate && cd /home2/genzcons/orthobestcarehub.co.ke
   ```

---

## 💻 Step 3: Connect via SSH / Terminal & Clone Repository

1. In cPanel, open **Terminal** (or connect via SSH):
   ```bash
   ssh genzcons@your-server-ip
   ```
2. Activate your virtual environment and navigate to the document root:
   ```bash
   source /home2/genzcons/virtualenv/orthobestcarehub.co.ke/3.12/bin/activate && cd /home2/genzcons/orthobestcarehub.co.ke
   ```
3. If this is a fresh setup and cPanel generated placeholder files (like `passenger_wsgi.py` or default HTML):
   ```bash
   # Remove default placeholder files:
   rm -rf * .env*
   
   # Clone the production repository from GitHub into the current directory:
   git clone https://github.com/cybertechocean/OrthobestCareHub.git .
   ```
   *If updating an existing deployment later, simply run:*
   ```bash
   git pull origin main
   ```

---

## 🔐 Step 4: Configure Production Environment Variables (`.env`)

1. Copy the production template `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env`:
   ```bash
   nano .env
   ```
3. Populate with your exact production values:
   ```ini
   # ---------------------------------------------------------------------------
   # CORE DJANGO SECURITY
   # ---------------------------------------------------------------------------
   DEBUG=False
   SECRET_KEY=generate-a-strong-random-50-character-secret-key-here
   ALLOWED_HOSTS=orthobestcarehub.co.ke,www.orthobestcarehub.co.ke,localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://orthobestcarehub.co.ke,https://www.orthobestcarehub.co.ke
   SECURE_SSL_REDIRECT=True

   # ---------------------------------------------------------------------------
   # MARIADB / MYSQL DATABASE
   # ---------------------------------------------------------------------------
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=genzcons_orthobestcare
   DB_USER=genzcons_orthobestuser
   DB_PASSWORD=your_actual_mariadb_password_here
   DB_HOST=localhost
   DB_PORT=3306

   # ---------------------------------------------------------------------------
   # CACHING (Database Cache)
   # ---------------------------------------------------------------------------
   CACHE_TABLE=orthobest_cache_table

   # ---------------------------------------------------------------------------
   # EMAIL SMTP CONFIGURATION
   # ---------------------------------------------------------------------------
   # Option A: Domain Webmail (info@orthobestcarehub.co.ke) - RECOMMENDED
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=mail.orthobestcarehub.co.ke
   EMAIL_PORT=465
   EMAIL_HOST_USER=info@orthobestcarehub.co.ke
   EMAIL_HOST_PASSWORD=your_email_password_here
   EMAIL_USE_TLS=False
   EMAIL_USE_SSL=True
   DEFAULT_FROM_EMAIL="Orthobest Care Hub <info@orthobestcarehub.co.ke>"

   # Option B: Google Workspace / Gmail (orthobestcarehub@gmail.com)
   # If using Gmail, generate a 16-character App Password at: myaccount.google.com/apppasswords
   # EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   # EMAIL_HOST=smtp.gmail.com
   # EMAIL_PORT=587
   # EMAIL_HOST_USER=orthobestcarehub@gmail.com
   # EMAIL_HOST_PASSWORD=your_16_char_app_password
   # EMAIL_USE_TLS=True
   # EMAIL_USE_SSL=False
   # DEFAULT_FROM_EMAIL="Orthobest Care Hub <orthobestcarehub@gmail.com>"

   # ---------------------------------------------------------------------------
   # SAFARICOM DARAJA M-PESA API (Kenyan Payments)
   # ---------------------------------------------------------------------------
   MPESA_ENVIRONMENT=live
   MPESA_CONSUMER_KEY=your_live_daraja_consumer_key
   MPESA_CONSUMER_SECRET=your_live_daraja_consumer_secret
   MPESA_PASSKEY=your_live_daraja_passkey
   MPESA_SHORTCODE=your_till_or_paybill_number
   MPESA_CALLBACK_URL=https://orthobestcarehub.co.ke/payments/mpesa/callback/

   # ---------------------------------------------------------------------------
   # BUSINESS DETAILS
   # ---------------------------------------------------------------------------
   SITE_NAME="Orthobest Care Hub"
   SITE_DOMAIN=orthobestcarehub.co.ke
   CONTACT_EMAIL=info@orthobestcarehub.co.ke
   CONTACT_EMAIL_ALT=orthobestcarehub@gmail.com
   SITE_PHONE="+254 719 160 398"
   SITE_PHONE_ALT="+254 727 480 198"
   WHATSAPP_NUMBER="254798246811"
   ```
4. Save and exit (`Ctrl + O`, then `Enter`, then `Ctrl + X`).
5. Secure permissions on `.env`:
   ```bash
   chmod 600 .env
   ```

---

## 📦 Step 5: Install Dependencies in Virtualenv

Ensure your virtualenv is active:
```bash
source /home2/genzcons/virtualenv/orthobestcarehub.co.ke/3.12/bin/activate && cd /home2/genzcons/orthobestcarehub.co.ke
```
Install all production requirements:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
> **MariaDB Driver**: The project includes `PyMySQL` and automatically initializes it in `orthobestcarehub/__init__.py` and `passenger_wsgi.py`. This guarantees zero compilation errors on shared hosting where gcc or mysql-devel headers are restricted.

---

## 🗄️ Step 6: Run Database Migrations

Apply all initial database tables to your MariaDB database:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ⚡ Step 7: Create Cache Table

Create the database table for Django's high-performance caching layer:
```bash
python manage.py createcachetable
```
*This creates the `orthobest_cache_table` inside `genzcons_orthobestcare` as defined in `settings.CACHES`.*

---

## 🌱 Step 8: Seed Store Catalog & Site Content

Populate MariaDB with all audited orthopedic products, rehabilitation equipment, Nairobi & countrywide delivery zones, hero slides, and site settings:
```bash
python manage.py populate_store
```

The automated seeder configures:
- Initial administrator account (`admin` / `admin1234`)
- Homepage Hero carousel slides & trust benefits
- Complete product categories with SEO meta tags
- Audited clinical products, variants, SKUs, and Kenya pricing
- Kenyan delivery zones (Nairobi CBD Free Pickups, Metro Express, Countrywide Courier)
- FAQs, services, and policies

---

## 🔑 Step 9: Change Administrator Password

Immediately update the administrator password for production:
```bash
python manage.py changepassword admin
```
Enter your new password when prompted.

---

## 🎨 Step 10: Collect Static Assets (WhiteNoise)

Compile and compress all stylesheets, icons, and JavaScript into `staticfiles/`:
```bash
python manage.py collectstatic --noinput
```
*WhiteNoise automatically manages caching headers and compression (gzip & brotli).*

---

## 📁 Step 11: Set Permissions & Passenger Restart

Ensure proper permissions for uploads and static files:
```bash
mkdir -p media staticfiles tmp
chmod -R 755 media staticfiles
```

Restart Phusion Passenger to reload the application:
```bash
# Method A: Terminal touch command
touch tmp/restart.txt

# Method B: In cPanel under "Setup Python App", click the "Restart" button for orthobestcarehub.co.ke
```

---

## ✅ Step 12: Verify Live Deployment

1. Open **`https://orthobestcarehub.co.ke/`** in your browser.
2. Verify:
   - **HTTPS / SSL**: Green padlock is active.
   - **Hero Carousel**: Smooth autoplay, Kenya branding, and high-impact CTAs.
   - **Mobile View**: Sticky bottom action bar (`SHOP` | `CALL` | `LOCATE`) appears exclusively on mobile screens with safe-area padding.
   - **Floating Speed-Dial**: Modern circular bottom-right button expands all 7 contact channels (Phone, WhatsApp, Email, Facebook, Instagram, X, YouTube) using FontAwesome for social icons and Lucide for UI icons.
   - **Admin Portal**: Accessible at **`https://orthobestcarehub.co.ke/admin/`** with Django Unfold styled in company brand colors (Deep Navy `#01174E` and Bright Gold `#FBD420`) and CKEditor 5.

---

## 🔄 Routine Deployment / Maintenance Commands

Whenever you push new changes to GitHub, update the live site via SSH in seconds:
```bash
# 1. Activate environment
source /home2/genzcons/virtualenv/orthobestcarehub.co.ke/3.12/bin/activate && cd /home2/genzcons/orthobestcarehub.co.ke

# 2. Pull latest code from GitHub
git pull origin main

# 3. Apply any new migrations
python manage.py migrate

# 4. Collect static changes
python manage.py collectstatic --noinput

# 5. Reload the live app
touch tmp/restart.txt
```
