# OLD SITE AUDIT — ORTHOBEST CARE REHAB

**Audit Date:** August 26, 2026  
**Old Domain:** `orthobestcarerehab.co.ke`  
**New Domain:** `orthobestcarehub.co.ke`  
**Target Entity:** Orthobest Care Hub (formerly Orthobest Care Hab / Rehab)  

---

## 1. Verified Business Profile & Identity

| Attribute | Audited Detail |
| :--- | :--- |
| **Business Name** | Orthobest Care Hub (Registered in Kenya as Orthobest Care Hab) |
| **Physical Address** | Mfangano Street, Travis Building, 3rd Floor, Room C37, Wing C (Adjacent to Quickmart Supermarket), Nairobi CBD, Kenya |
| **Primary Phone** | `+254 719 160 398` / `+254 727 480 198` |
| **WhatsApp Line** | `+254 798 246 811` / `+254 719 160 398` |
| **Official Email** | `info@orthobestcarehub.co.ke` / `info@orthobestcarerehab.co.ke` |
| **Working Hours** | Mon – Fri: 9:00 AM – 5:00 PM | Sat: 9:00 AM – 3:00 PM | Sun & Public Holidays: Closed |
| **Target Audience** | Patients recovering from injury/surgery, physiotherapy clients, elderly individuals, mobility aid users, hospitals, clinics, and home caregivers in Kenya. |

---

## 2. Product Categories & Specialties

1. **Mobility Aids**
   - Standard & Lightweight Manual Wheelchairs
   - Cerebral Palsy (CP) Specialized Wheelchairs
   - Aluminum Walking Sticks & Quad Canes
   - Underarm & Elbow Crutches
   - Rollators & Walkers

2. **Orthopedic Supports & Braces**
   - Adjustable Cervical Collars
   - Wrist & Forearm Splints / Braces
   - Knee Hinged & Neoprene Stabilizers
   - Lumbo-Sacral Support Belts / Back Guards
   - Ankle Supports & Stirrup Braces
   - Clavicle / Posture Correctors

3. **Rehabilitation & Physiotherapy Equipment**
   - Digital Mini Pedal Exercisers (Arm & Leg)
   - Heavy-duty Standing Aid Frames
   - Medical Goniometers
   - TheraBand Resistance Elastic Bands & Loops
   - Hand Grip & Finger Exercisers
   - Percussion Massage Guns / Fascial Guns
   - Cupping Therapy Sets

4. **Medical Furniture & Hospital Supplies**
   - Manual & Electric Hospital Beds (1-Cranks & 2-Cranks)
   - Overbed Tables & IV Drip Stands
   - Wheelchair Cushions & Anti-bedsore Air Mattresses
   - ICU Patient Monitoring Accessories

5. **Daily Living & Homecare**
   - Commode Chairs (Foldable & Mobile)
   - Shower & Bath Chairs
   - Adult Disposable Underpads & Bed Incontinence Sheets

---

## 3. Verified Sample Pricing (from Audited Records)

| Product Item | Audited Price (KSh) | Category |
| :--- | :--- | :--- |
| Standard Manual Folding Wheelchair | KSh 13,000 | Mobility Aids |
| Adjustable Aluminum Walking Stick | KSh 1,800 | Mobility Aids |
| Wrist & Forearm Support Brace / Splint | KSh 2,750 | Orthopedic Supports |
| Adjustable Cervical Collar (Neck Brace) | KSh 4,000 | Orthopedic Supports |
| Lumbar Sacral Spine Support Belt | KSh 3,200 | Orthopedic Supports |
| Hinged Knee Support Brace | KSh 3,800 | Orthopedic Supports |
| Digital Arm & Leg Pedal Exerciser | KSh 9,000 | Rehabilitation & Physio |
| Standing Aid Rehabilitation Frame | KSh 25,000 | Rehabilitation & Physio |
| Percussion Massage Fascial Gun | KSh 4,500 | Rehabilitation & Physio |
| TheraBand Resistance Band Set | KSh 2,200 | Rehabilitation & Physio |
| Foldable Commode Bedside Chair | KSh 6,500 | Daily Living & Homecare |
| Premium Adult Disposable Underpads (Pack) | KSh 1,200 | Daily Living & Homecare |

---

## 4. URL Migration & 301 Redirection Map

| Old URL Pattern (`orthobestcarerehab.co.ke`) | New URL Pattern (`orthobestcarehub.co.ke`) | HTTP Status |
| :--- | :--- | :--- |
| `/` | `/` | 301 |
| `/shop/` | `/shop/` | 301 |
| `/product-category/mobility-aids/` | `/shop/category/mobility-aids/` | 301 |
| `/product-category/orthopedic-supports/` | `/shop/category/orthopedic-supports/` | 301 |
| `/product-category/rehabilitation/` | `/shop/category/rehabilitation-equipment/` | 301 |
| `/product-category/hospital-furniture/` | `/shop/category/medical-furniture/` | 301 |
| `/product-category/home-care/` | `/shop/category/home-care/` | 301 |
| `/product/<slug>/` | `/product/<slug>/` | 301 |
| `/about-us/` | `/about/` | 301 |
| `/contact-us/` | `/contact/` | 301 |
| `/services/` | `/services/` | 301 |
| `/blog/` | `/blog/` | 301 |
| `/faq/` | `/faq/` | 301 |

---

## 5. Items Requiring Ongoing Business Owner Confirmation

1. **M-Pesa Paybill / Till Number & Daraja API Credentials**: Fully abstracted via environment variables (`MPESA_CONSUMER_KEY`, `MPESA_PASSKEY`, `MPESA_SHORTCODE`, etc.) so the owner can plug in live Daraja keys or Till details.
2. **Delivery Fee Zones**: Default configured with Kenyan counties/cities (Nairobi CBD: Free/KSh 200, Nairobi Suburbs: KSh 300, Kiambu/Machakos: KSh 400, Upcountry/Courier: KSh 600) — fully manageable in Django Admin.
3. **Card & Bank Payment Gateways**: Modular payment architecture ready for Pesapal / Stripe / Bank transfer / Pay on Delivery.
