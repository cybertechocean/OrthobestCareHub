# 🚀 Orthobest Care Hub — Shared Hosting Deployment Guide

Complete step-by-step production deployment manual for **Orthobest Care Hub** on shared hosting (cPanel with CloudLinux / Phusion Passenger).

---

## 📌 Deployment Specifications

| Parameter | Production Value |
| :--- | :--- |
| **Domain Name** | `orthobestcarehub.co.ke` (and `www.orthobestcarehub.co.ke`) |
| **GitHub Repository** | `https://github.com/cybertechocean/OrthobestCareHub` |
| **Application Directory** | `/home/orthobes/OrthobestCareHub` |
| **Python Virtualenv** | `/home/orthobes/virtualenv/OrthobestCareHub/3.11/` |
| **Python Version** | `3.11` |
| **Database Engine** | MariaDB / MySQL |
| **Database Name** | `orthobestcare` (or cPanel prefixed e.g. `orthobes_orthobestcare`) |
| **Database User** | `orthobestuser` (or cPanel prefixed e.g. `orthobes_orthobestuser`) |
| **WSGI Entry Point** | `passenger_wsgi.py` |
| **Static Handling** | WhiteNoise (`CompressedManifestStaticFilesStorage`) |
| **Cache System** | Django DatabaseCache (`orthobest_cache_table`) |

---

## 🛠️ Step 1: Create MariaDB Database & User in cPanel

1. Log in to your **cPanel** dashboard.
2. Navigate to **Databases** → **MySQL® Databases** (or **MariaDB Databases**).
3. Under **Create New Database**:
   - Database Name: `orthobestcare` (note if cPanel adds prefix `orthobes_orthobestcare`).
   - Click **Create Database**.
4. Under **Add New User**:
   - Username: `orthobestuser`
   - Password: generate a strong password and save it securely for `.env`.
   - Click **Create User**.
5. Under **Add User To Database**:
   - Select user `orthobestuser` and database `orthobestcare`.
   - Click **Add**.
   - Check **ALL PRIVILEGES** and click **Make Changes**.

---

## 🐍 Step 2: Configure Python App in cPanel

1. In cPanel, navigate to **Software** → **Setup Python App**.
2. Click **Create Application**.
3. Fill in the parameters:
   - **Python version**: `3.11`
   - **Application root**: `OrthobestCareHub` (this corresponds to `/home/orthobes/OrthobestCareHub`)
   - **Application URL**: `orthobestcarehub.co.ke`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
4. Click **Create** (top right).
5. cPanel will display a command to activate the virtual environment at the top of the page, e.g.:
   ```bash
   source /home/orthobes/virtualenv/OrthobestCareHub/3.11/bin/activate && cd /home/orthobes/OrthobestCareHub
   ```

---

## 💻 Step 3: Clone or Pull Code via SSH / Terminal

1. In cPanel, open **Terminal** (or connect via SSH):
   ```bash
   ssh orthobes@your-server-ip
   ```
2. Activate your virtual environment:
   ```bash
   source /home/orthobes/virtualenv/OrthobestCareHub/3.11/bin/activate && cd /home/orthobes/OrthobestCareHub
   ```
3. If setting up for the first time:
   ```bash
   # If the directory already has default cPanel files, remove them:
   rm -rf * .env*
   # Clone the repository:
   git clone https://github.com/cybertechocean/OrthobestCareHub.git .
   ```
   If updating an existing deployment:
   ```bash
   git pull origin main
   ```

---

## 🔐 Step 4: Configure Production Environment Variables (`.env`)

1. Copy the example configuration file:
   ```bash
   cp .env.example .env
   ```
2. Open and edit `.env` using nano or cPanel File Manager:
   ```bash
   nano .env
   ```
3. Update the values with your actual production secrets:
   ```ini
   # Core Django
   DEBUG=False
   SECRET_KEY=paste-your-generated-50-character-secret-key-here
   ALLOWED_HOSTS=orthobestcarehub.co.ke,www.orthobestcarehub.co.ke,localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://orthobestcarehub.co.ke,https://www.orthobestcarehub.co.ke
   SECURE_SSL_REDIRECT=True

   # MariaDB / MySQL Configuration
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=orthobestcare        # Or orthobes_orthobestcare if prefixed
   DB_USER=orthobestuser        # Or orthobes_orthobestuser if prefixed
   DB_PASSWORD=your_actual_database_password
   DB_HOST=localhost
   DB_PORT=3306

   # Cache Table
   CACHE_TABLE=orthobest_cache_table

   # Email SMTP (cPanel Mail)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=mail.orthobestcarehub.co.ke
   EMAIL_PORT=465
   EMAIL_HOST_USER=info@orthobestcarehub.co.ke
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=False
   EMAIL_USE_SSL=True
   DEFAULT_FROM_EMAIL="Orthobest Care Hub <info@orthobestcarehub.co.ke>"

   # Kenyan M-Pesa Safaricom Daraja API
   MPESA_ENVIRONMENT=live
   MPESA_CONSUMER_KEY=your_daraja_consumer_key
   MPESA_CONSUMER_SECRET=your_daraja_consumer_secret
   MPESA_PASSKEY=your_daraja_passkey
   MPESA_SHORTCODE=your_till_or_paybill_number
   MPESA_CALLBACK_URL=https://orthobestcarehub.co.ke/payments/mpesa/callback/
   ```
4. Save and exit (`Ctrl + O`, then `Enter`, then `Ctrl + X` in nano).
5. Secure permissions on `.env`:
   ```bash
   chmod 600 .env
   ```

---

## 📦 Step 5: Install Python Dependencies

With your virtual environment active:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note on MariaDB Driver**: The project includes `PyMySQL` and initializes it in `orthobestcarehub/__init__.py` and `passenger_wsgi.py`. This guarantees zero compilation errors on shared hosting where C-compiler (`gcc`) or `mysql-devel` headers are restricted.

---

## 🗄️ Step 6: Run Database Migrations

Apply all database tables to MariaDB:
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
This creates `orthobest_cache_table` in MariaDB as specified by `settings.CACHES`.

---

## 🌱 Step 8: Seed Store Data (Products, Categories, Kenyan Delivery Zones)

Populate the database with all audited orthopedic products, rehabilitation equipment, delivery rates (Nairobi & countrywide), and site settings:
```bash
python manage.py populate_store
```

This automated seeder creates:
- Default administrator (`admin` / `admin1234`)
- Hero slides & benefits
- Complete product categories with SEO meta descriptions
- Audited clinical products, variants, and pricing
- Kenyan delivery zones (Nairobi CBD Free Pickups, Metro Express, Countrywide Courier)
- Trust badges, FAQs, and store policies

---

## 🔑 Step 9: Change Default Admin Password

Immediately update the administrator password for production:
```bash
python manage.py changepassword admin
```
Enter your new secure password when prompted.

---

## 🎨 Step 10: Collect Static Assets (WhiteNoise)

Compile and compress all stylesheets, JavaScript scripts, and icons into `staticfiles/`:
```bash
python manage.py collectstatic --noinput
```
WhiteNoise will bundle and compress all assets using gzip & brotli.

---

## 📁 Step 11: Set Permissions for Media and Uploads

Ensure web server process can read and write uploaded media files:
```bash
mkdir -p media staticfiles tmp
chmod -R 755 media staticfiles
```

---

## 🔄 Step 12: Restart the Application

Restart the Passenger WSGI server:
```bash
# Option A: Via Terminal (touch restart)
mkdir -p tmp && touch tmp/restart.txt

# Option B: Via cPanel Dashboard
# Go to "Setup Python App" -> Click "Restart" button next to orthobestcarehub.co.ke
```

---

## ✅ Step 13: Verify Live Deployment

1. Visit **`https://orthobestcarehub.co.ke/`** in your browser.
2. Confirm:
   - Homepage loads with SSL padlock.
   - Products, Hero carousel, and trust badges render properly.
   - Mobile Sticky Bottom Action Bar (`SHOP` | `CALL` | `LOCATE`) appears on mobile devices.
   - Floating Contact / Social Speed-Dial button unfurls on click with FontAwesome brand icons.
   - Admin portal is accessible at **`https://orthobestcarehub.co.ke/admin/`** with Django Unfold styling and company brand colors.

---

## 🚨 Troubleshooting Common Shared Hosting Issues

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| **500 Internal Server Error** | Missing `.env` or syntax error | Check `stderr.log` in `/home/orthobes/OrthobestCareHub/stderr.log` |
| **Database Connection Error (2002/2003)** | MariaDB credentials mismatch | Verify `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in `.env`. Ensure cPanel prefix is included if applicable (e.g. `orthobes_orthobestcare`). |
| **DisallowedHost Error** | Domain not in `ALLOWED_HOSTS` | Ensure `ALLOWED_HOSTS` in `.env` includes `orthobestcarehub.co.ke,www.orthobestcarehub.co.ke`. |
| **CSS/JS Not Loading** | Static files not collected | Run `python manage.py collectstatic --noinput` and touch `tmp/restart.txt`. |
| **CSRF Verification Failed** | Missing CSRF origin | Ensure `CSRF_TRUSTED_ORIGINS=https://orthobestcarehub.co.ke,https://www.orthobestcarehub.co.ke` is in `.env`. |
| **Images 404** | Missing media permissions | Run `chmod -R 755 media/` |

---

## 🔄 Routine Deployment / Maintenance Commands

For any subsequent updates:
```bash
# 1. Activate environment
source /home/orthobes/virtualenv/OrthobestCareHub/3.11/bin/activate && cd /home/orthobes/OrthobestCareHub

# 2. Pull latest code
git pull origin main

# 3. Apply any new migrations
python manage.py migrate

# 4. Collect static changes
python manage.py collectstatic --noinput

# 5. Restart application
touch tmp/restart.txt
```
