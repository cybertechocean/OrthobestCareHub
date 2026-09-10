from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.models import (
    SiteSettings, HomeBanner, TrustBadge,
    HeroSlide, HeroSlideBenefit, HeroCarouselSettings
)
from apps.products.models import Category, Brand, Product, ProductImage, ProductVariant, ProductReview
from apps.orders.models import DeliveryZone, Coupon
from apps.content_hub.models import Service, BlogCategory, BlogPost, FAQ, LegalPage

User = get_user_model()


class Command(BaseCommand):
    help = "Populates database with audited Kenyan healthcare products, categories, delivery zones, and settings"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Populating Orthobest Care Hub database..."))

        # 1. Create or get Admin User
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                'email': "info@orthobestcarehub.co.ke",
                'first_name': "Orthobest",
                'last_name': "Admin",
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password("admin1234")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin1234"))

        # 2. Setup Site Settings
        settings, _ = SiteSettings.objects.get_or_create(id=1)
        settings.site_name = "Orthobest Care Hub"
        settings.site_domain = "orthobestcarehub.co.ke"
        settings.tagline = "Kenya's Trusted Destination for Orthopedic, Rehabilitation & Mobility Products"
        settings.phone_primary = "+254 719 160 398"
        settings.phone_secondary = "+254 727 480 198"
        settings.whatsapp_number = "254798246811"
        settings.contact_email = "info@orthobestcarehub.co.ke"
        settings.physical_address = "Mfangano Street, Travis Building, 3rd Floor, Room C37, Wing C (near Quickmart), Nairobi CBD, Kenya"
        settings.business_hours = "Mon - Fri: 9:00 AM - 5:00 PM | Sat: 9:00 AM - 3:00 PM | Sun: Closed"
        settings.announcement_bar_enabled = True
        settings.announcement_bar_text = "🚚 Swift, Secure Delivery Across Kenya | Call or WhatsApp 0798 246 811 for Expert Sizing Support"
        settings.announcement_bar_link = "/shop/"
        settings.hero_headline = "SUPPORT YOUR MOVEMENT. LIVE WITH CONFIDENCE."
        settings.hero_subheadline = "Explore Kenya's highest quality orthopedic braces, rehabilitation equipment, manual & electric wheelchairs, and clinical homecare essentials."
        settings.medical_disclaimer = "Product information provided on this platform is for educational and purchasing guidance only and does not substitute professional orthopedic evaluation. Please consult your physician or physiotherapist for injury diagnoses."
        settings.save()

        # 2b. Setup Hero Carousel Settings & Slides
        carousel_settings = HeroCarouselSettings.get_settings()
        carousel_settings.autoplay = True
        carousel_settings.autoplay_speed = 5500
        carousel_settings.show_arrows = True
        carousel_settings.show_indicators = True
        carousel_settings.pause_on_hover = True
        carousel_settings.transition_speed = 600
        carousel_settings.loop_slides = True
        carousel_settings.save()

        HeroSlide.objects.all().delete()

        # Slide 1: Main Reference Brand Slide
        slide1 = HeroSlide.objects.create(
            title="Homepage Hero Slide - Main Brand & Orthopedic Store",
            badge_icon="✦",
            badge_text="KENYA'S #1 ORTHOPEDIC & REHAB STORE",
            heading="SUPPORT YOUR MOVEMENT.\nLIVE WITH CONFIDENCE.",
            description="Explore Kenya's highest quality orthopedic braces, rehabilitation equipment, manual & electric wheelchairs, and clinical homecare essentials.",
            primary_button_text="Shop Products →",
            primary_button_url="/shop/",
            secondary_button_text="Talk to a Specialist",
            secondary_button_url="/contact/",
            image="hero_slides/hero_slide_1.jpg",
            image_alt_text="Orthobest Care Hub Orthopedic & Rehabilitation Products Nairobi Kenya",
            order=1,
            is_active=True,
        )
        HeroSlideBenefit.objects.create(hero_slide=slide1, icon="✓", text="Medical Graded", order=1)
        HeroSlideBenefit.objects.create(hero_slide=slide1, icon="✓", text="M-Pesa Friendly", order=2)
        HeroSlideBenefit.objects.create(hero_slide=slide1, icon="✓", text="Doorstep Delivery", order=3)

        # Slide 2: Mobility & Wheelchairs
        slide2 = HeroSlide.objects.create(
            title="Homepage Hero Slide - Mobility & Wheelchair Solutions",
            badge_icon="♿",
            badge_text="LIGHTWEIGHT & ELECTRIC MOBILITY SOLUTIONS",
            heading="INDEPENDENCE AT EVERY STEP.\nBUILT FOR KENYAN TERRAINS.",
            description="Discover durable standard manual wheelchairs, pediatric CP chairs, ergonomic crutches, and motorized mobility aids with nationwide delivery.",
            primary_button_text="Explore Wheelchairs →",
            primary_button_url="/shop/category/mobility-aids/",
            secondary_button_text="Talk to a Specialist",
            secondary_button_url="/contact/",
            image="hero_slides/hero_slide_1.jpg",
            image_alt_text="Wheelchairs and mobility aids Nairobi Kenya",
            order=2,
            is_active=True,
        )
        HeroSlideBenefit.objects.create(hero_slide=slide2, icon="✓", text="Certified Durability", order=1)
        HeroSlideBenefit.objects.create(hero_slide=slide2, icon="✓", text="WhatsApp Sizing Support", order=2)
        HeroSlideBenefit.objects.create(hero_slide=slide2, icon="✓", text="Nationwide Courier", order=3)

        # Slide 3: Clinical Supports & Recovery
        slide3 = HeroSlide.objects.create(
            title="Homepage Hero Slide - Clinical Supports & Braces",
            badge_icon="🩺",
            badge_text="CLINICAL GRADE RECOVERY GEAR",
            heading="TARGETED PAIN RELIEF.\nACCELERATE YOUR RECOVERY.",
            description="Anatomical knee braces, post-surgery lumbar supports, cervical collars, and physiotherapy recovery systems recommended by orthopedic specialists.",
            primary_button_text="Shop Orthopedic Supports →",
            primary_button_url="/shop/category/orthopedic-supports/",
            secondary_button_text="Consult Specialist",
            secondary_button_url="/contact/",
            image="hero_slides/hero_slide_1.jpg",
            image_alt_text="Orthopedic braces and support gear Nairobi",
            order=3,
            is_active=True,
        )
        HeroSlideBenefit.objects.create(hero_slide=slide3, icon="✓", text="Physiotherapist Approved", order=1)
        HeroSlideBenefit.objects.create(hero_slide=slide3, icon="✓", text="Easy Adjustability", order=2)
        HeroSlideBenefit.objects.create(hero_slide=slide3, icon="✓", text="Pay on Delivery in Nairobi", order=3)

        # 3. Setup Trust Badges
        TrustBadge.objects.all().delete()
        badges_data = [
            {"title": "100% Certified Quality", "subtitle": "Durable, medically graded supports & appliances", "icon_svg": "shield-check", "display_order": 1},
            {"title": "Kenya-Wide Fast Delivery", "subtitle": "Same-day delivery in Nairobi & 24h courier countrywide", "icon_svg": "truck", "display_order": 2},
            {"title": "Direct WhatsApp Support", "subtitle": "Instant sizing & product advice from our staff", "icon_svg": "message-circle", "display_order": 3},
            {"title": "Safe M-Pesa & Cash on Delivery", "subtitle": "Zero hassle STK Push, Paybill, or Pay on Arrival", "icon_svg": "credit-card", "display_order": 4},
        ]
        for b in badges_data:
            TrustBadge.objects.create(**b)

        # 4. Setup Home Banners
        HomeBanner.objects.all().delete()
        banners_data = [
            {
                "title": "Mobility Solutions for Greater Independence",
                "subtitle": "Discover lightweight manual wheelchairs, pediatric CP chairs, and ergonomic walking aids built for Kenyan terrains.",
                "badge_text": "Top Recommended Mobility",
                "button_text": "View Wheelchairs & Aids",
                "button_link": "/shop/category/mobility-aids/",
                "bg_gradient": "linear-gradient(135deg, #0f766e 0%, #064e3b 100%)",
                "display_order": 1,
            },
            {
                "title": "Clinical-Grade Orthopedic Supports",
                "subtitle": "Targeted stabilization for post-surgery recovery, ligament tears, arthritis, and chronic back/neck pain.",
                "badge_text": "Recovery & Comfort",
                "button_text": "Explore Braces",
                "button_link": "/shop/category/orthopedic-supports/",
                "bg_gradient": "linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%)",
                "display_order": 2,
            },
        ]
        for ban in banners_data:
            HomeBanner.objects.create(**ban)

        # 5. Setup Delivery Zones
        DeliveryZone.objects.all().delete()
        zones = [
            {"name": "Nairobi CBD & Immediate Surroundings", "delivery_fee": Decimal("200.00"), "estimated_delivery_time": "2 - 4 Hours", "display_order": 1},
            {"name": "Nairobi Suburbs (Westlands, Karen, Kilimani, Kasarani, etc.)", "delivery_fee": Decimal("300.00"), "estimated_delivery_time": "Same Day (Within 6 Hours)", "display_order": 2},
            {"name": "Kiambu & Machakos Environs (Thika, Ruiru, Kikuyu, Athi River)", "delivery_fee": Decimal("450.00"), "estimated_delivery_time": "Same Day / Next Day Morning", "display_order": 3},
            {"name": "Upcountry Kenya Courier (Mombasa, Kisumu, Nakuru, Eldoret, etc.)", "delivery_fee": Decimal("600.00"), "estimated_delivery_time": "24 - 48 Hours via Fargo/G4S/Courier", "display_order": 4},
        ]
        for z in zones:
            DeliveryZone.objects.create(**z)

        # 6. Setup Coupons
        Coupon.objects.all().delete()
        Coupon.objects.create(
            code="WELCOME10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            minimum_order=Decimal("2000.00"),
            maximum_discount=Decimal("2000.00"),
            active=True
        )
        Coupon.objects.create(
            code="REHAB500",
            discount_type="fixed",
            discount_value=Decimal("500.00"),
            minimum_order=Decimal("5000.00"),
            active=True
        )

        # 7. Setup Categories
        Category.objects.all().delete()
        categories_data = [
            {
                "name": "Mobility Aids",
                "slug": "mobility-aids",
                "description": "Standard & lightweight folding wheelchairs, pediatric cerebral palsy wheelchairs, crutches, walking sticks, rollators, and mobility accessories.",
                "icon_name": "wheelchair",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "name": "Orthopedic Supports & Braces",
                "slug": "orthopedic-supports",
                "description": "Anatomical knee braces, cervical neck collars, wrist & forearm splints, lumbar sacral support belts, ankle supports, and posture aligners.",
                "icon_name": "activity",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "name": "Rehabilitation & Physiotherapy",
                "slug": "rehabilitation-equipment",
                "description": "Digital pedal exercisers, heavy-duty standing frames, goniometers, resistance TheraBands, percussion massage guns, and exercise therapy devices.",
                "icon_name": "heart-pulse",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "name": "Medical Furniture & Hospital Supplies",
                "slug": "medical-furniture",
                "description": "Manual & electric hospital beds, overbed tables, drip IV stands, anti-decubitus air mattresses, and clinic observation furnishings.",
                "icon_name": "bed",
                "is_featured": True,
                "display_order": 4,
            },
            {
                "name": "Daily Living & Home Care",
                "slug": "home-care",
                "description": "Bedside commode chairs, shower chairs, adult disposable underpads, patient transfer aids, and homecare wellness solutions.",
                "icon_name": "shield",
                "is_featured": True,
                "display_order": 5,
            },
        ]
        created_categories = {}
        for c in categories_data:
            cat = Category.objects.create(**c)
            created_categories[c['slug']] = cat

        # 8. Setup Brands
        Brand.objects.all().delete()
        brands_data = ["Orthobest Pro", "Vissco Healthcare", "Flamingo Health", "Dyna Orthotics", "CareQuip Medical"]
        created_brands = {}
        for b_name in brands_data:
            brand = Brand.objects.create(name=b_name)
            created_brands[b_name] = brand

        # 9. Setup Audited Products
        Product.objects.all().delete()
        products_data = [
            {
                "name": "Standard Manual Folding Wheelchair with Padded Armrests",
                "slug": "standard-manual-folding-wheelchair",
                "sku": "OBC-MW-001",
                "category": created_categories["mobility-aids"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("13000.00"),
                "compare_at_price": Decimal("15000.00"),
                "cost_price": Decimal("9500.00"),
                "stock_quantity": 12,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Durable steel-frame manual wheelchair designed for comfort and everyday mobility across Kenyan indoor and outdoor environments.",
                "description": "The Orthobest Standard Folding Wheelchair is constructed from heavy-duty chrome-plated steel, featuring puncture-proof solid rubber rear wheels and smooth front castors. Includes dual hand brakes, flip-up footrests with heel loops, and breathable PVC upholstery that is easy to sanitize.",
                "features": "• Heavy-duty chrome/powder-coated steel frame\n• Easily foldable for vehicle trunk transport\n• Padded armrests with side protective skirts\n• Swing-away footrests with adjustable calf support\n• Solid 24-inch rear wheels with ergonomic push rims\n• Weight capacity: Up to 120 kg",
                "specifications": "Material: Steel alloy frame & vinyl upholstery\nSeat Width: 18 inches (46 cm)\nTotal Weight: 16.5 kg\nFolded Width: 28 cm\nMax User Weight: 120 kg",
                "how_to_use": "Unfold by pressing downward on the outer edges of the seat upholstery until fully locked. Secure brakes before assisting the user into or out of the chair.",
                "size_guide": "Standard adult size (18-inch seat). Accommodates users weighing between 45 kg and 120 kg comfortably.",
            },
            {
                "name": "Adjustable Aluminum Walking Stick with Ergonomic Handle",
                "slug": "adjustable-aluminum-walking-stick",
                "sku": "OBC-WS-002",
                "category": created_categories["mobility-aids"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("1800.00"),
                "compare_at_price": Decimal("2200.00"),
                "cost_price": Decimal("1100.00"),
                "stock_quantity": 30,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Lightweight height-adjustable walking cane with anti-slip rubber tip and contoured palm grip for steady walking balance.",
                "description": "Crafted from aircraft-grade anodized aluminum, this walking cane provides reliable balance support for seniors and rehabilitation patients recovering from lower limb injuries.",
                "features": "• 10-level push-button height adjustment\n• Non-slip heavy-duty rubber ferrule base\n• Ergonomic T-handle reduces wrist strain\n• Safety wrist strap included",
                "specifications": "Material: Anodized Aluminum\nAdjustable Height: 75 cm – 98 cm\nProduct Weight: 350 g\nWeight Capacity: Up to 110 kg",
                "how_to_use": "Adjust the pin so that when your arm is resting at your side, the top of the handle aligns with your wrist crease.",
                "size_guide": "One size fits all adults (height adjustable from 4'10\" to 6'4\").",
            },
            {
                "name": "Adjustable Cervical Collar (Rigid Neck Support)",
                "slug": "adjustable-cervical-collar-rigid",
                "sku": "OBC-CC-003",
                "category": created_categories["orthopedic-supports"],
                "brand": created_brands["Flamingo Health"],
                "price": Decimal("4000.00"),
                "compare_at_price": Decimal("4800.00"),
                "cost_price": Decimal("2800.00"),
                "stock_quantity": 18,
                "is_featured": True,
                "is_bestseller": False,
                "is_new": True,
                "short_description": "Multi-height adjustable rigid cervical collar engineered for cervical spine immobilization and post-trauma recovery.",
                "description": "Provides high immobilization of the cervical spine following whiplash injuries, disc herniation, cervical spondylosis, or post-surgical rehabilitation. Features ventilation slots and a trachea opening for air circulation and easy clinical monitoring.",
                "features": "• 4-stage easy click height adjustment\n• Large trachea opening for ventilation and airway access\n• X-ray and CT-scan translucent materials\n• Antimicrobial foam padding resists moisture buildup",
                "specifications": "Material: High-density polyethylene & closed-cell foam\nSizes: Multi-position universal adjustment",
                "how_to_use": "Position the chin piece securely under the patient's chin, wrap the posterior support around the back of the neck, and secure with Velcro straps.",
                "size_guide": "Universal adult fitting with 4 height adjustments (Short, Regular, Tall, Extra Tall).",
            },
            {
                "name": "Rigid Wrist & Forearm Splint / Brace (Bilateral)",
                "slug": "rigid-wrist-forearm-splint-brace",
                "sku": "OBC-WB-004",
                "category": created_categories["orthopedic-supports"],
                "brand": created_brands["Vissco Healthcare"],
                "price": Decimal("2750.00"),
                "compare_at_price": Decimal("3200.00"),
                "cost_price": Decimal("1800.00"),
                "stock_quantity": 25,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Anatomical wrist brace with aluminum palmar stay for carpal tunnel syndrome, sprains, tendonitis, and wrist fractures.",
                "description": "Designed to maintain the wrist in a neutral resting angle, reducing pain and pressure on the median nerve in carpal tunnel syndrome. Equipped with a removable contourable aluminum splint.",
                "features": "• Removable palmar splint provides rigid anatomical support\n• Breathable air-mesh fabric keeps skin cool and dry\n• Tri-strap compression system ensures customized fit\n• Relieves carpal tunnel, arthritis, and repetitive strain",
                "specifications": "Material: Neoprene, nylon, aluminum splint\nSide: Left / Right available",
                "how_to_use": "Slip hand into the brace with the aluminum splint resting along the palm. Fasten the middle strap first, then wrist and forearm straps.",
                "size_guide": "Measure wrist circumference:\nSmall: 13-16 cm | Medium: 16-19 cm | Large: 19-22 cm | XL: 22-25 cm",
            },
            {
                "name": "Lumbar Sacral Spine Support Belt with Dual Pull Straps",
                "slug": "lumbar-sacral-spine-support-belt",
                "sku": "OBC-LS-005",
                "category": created_categories["orthopedic-supports"],
                "brand": created_brands["Dyna Orthotics"],
                "price": Decimal("3200.00"),
                "compare_at_price": Decimal("3800.00"),
                "cost_price": Decimal("2100.00"),
                "stock_quantity": 20,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Ergonomic back support brace with 4 flexible splints and double-tension compression straps for sciatica and lower back pain.",
                "description": "Reinforced lower back stabilizer belt designed to decompress the lumbar spine, correct posture during heavy lifting, and alleviate sciatica, slip disc, and chronic lumbago.",
                "features": "• 4 contoured flexible lumbar stays\n• Dual elastic pull bands for targeted extra compression\n• Non-sweat breathable micro-mesh fabric\n• Low-profile design can be worn under daily work clothing",
                "specifications": "Material: Breathable elastic strap, silicone stays, Velcro\nHeight: 23 cm lumbar coverage",
                "how_to_use": "Center the stays over your lower spine, wrap the wide base belt around the abdomen and fasten, then pull secondary straps for desired tightness.",
                "size_guide": "Measure waist circumference at the belly button:\nS: 70-80 cm | M: 80-90 cm | L: 90-100 cm | XL: 100-110 cm | XXL: 110-125 cm",
            },
            {
                "name": "Hinged Knee Support Brace with Polycentric Lateral Bars",
                "slug": "hinged-knee-support-brace-polycentric",
                "sku": "OBC-KB-006",
                "category": created_categories["orthopedic-supports"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("3800.00"),
                "compare_at_price": Decimal("4500.00"),
                "cost_price": Decimal("2400.00"),
                "stock_quantity": 15,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": True,
                "short_description": "Heavy-duty dual-hinge knee stabilizer for ACL/MCL ligament injuries, meniscus tears, and post-operative knee protection.",
                "description": "Dual aluminum polycentric hinges closely mirror the natural glide motion of the human knee joint, preventing hyperextension and medial/lateral instability.",
                "features": "• Aircraft aluminum dual polycentric hinges\n• Open patella ring with silicone cushioning pad\n• Top and bottom counter-locking Velcro straps\n• Neoprene thermal insulation accelerates tendon recovery",
                "specifications": "Material: 4mm medical neoprene, aluminum alloy hinges\nWeight: 420 g",
                "how_to_use": "Center patella ring over kneecap, fasten wrap panels behind thigh and calf, then lock opposing straps.",
                "size_guide": "Measure circumference 10 cm above mid-kneecap:\nS: 34-39 cm | M: 39-44 cm | L: 44-49 cm | XL: 49-54 cm",
            },
            {
                "name": "Digital Mini Pedal Exerciser for Arm & Leg Rehabilitation",
                "slug": "digital-mini-pedal-exerciser",
                "sku": "OBC-PE-007",
                "category": created_categories["rehabilitation-equipment"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("9000.00"),
                "compare_at_price": Decimal("11000.00"),
                "cost_price": Decimal("6200.00"),
                "stock_quantity": 8,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Compact motorized/manual pedal trainer with LCD multi-function monitor for stroke recovery and low-impact cardiovascular therapy.",
                "description": "Ideal for seated physiotherapy at home or in clinical rehabilitation. Strengthens quadriceps, calves, shoulders, and arms without joint impact.",
                "features": "• Multi-function LCD: Speed, Time, Distance, Calories, RPM\n• Smooth stepless tension dial from gentle to high resistance\n• Non-slip rubber feet grips and adjustable foot straps\n• Can be placed on floor for leg pedaling or table for arm rehabilitation",
                "specifications": "Dimensions: 40 x 35 x 30 cm\nWeight: 4.8 kg\nPower: Battery operated LCD monitor (included)",
                "how_to_use": "Place securely on carpet or non-slip mat while seated in a sturdy chair. Pedal forward or backward as recommended by your physical therapist.",
                "size_guide": "Compact portable unit suitable for all adult patients.",
            },
            {
                "name": "Heavy-Duty Rehabilitation Standing Frame with Chest Support",
                "slug": "heavy-duty-rehabilitation-standing-frame",
                "sku": "OBC-SF-008",
                "category": created_categories["rehabilitation-equipment"],
                "brand": created_brands["CareQuip Medical"],
                "price": Decimal("25000.00"),
                "compare_at_price": Decimal("28500.00"),
                "cost_price": Decimal("18000.00"),
                "stock_quantity": 4,
                "is_featured": True,
                "is_bestseller": False,
                "is_new": True,
                "short_description": "Static rehabilitation standing frame assisting paraplegic, stroke, and cerebral palsy patients in upright weight-bearing therapy.",
                "description": "Crucial for preventing bone density loss, contractures, and pressure ulcers in immobile patients by providing secure therapeutic standing support.",
                "features": "• Adjustable pelvic and knee stabilization pads\n• Padded chest support harness with quick-release lock\n• Activity table tray for holding reading material or therapy items\n• 4 swivel lockable casters for safe room transfer",
                "specifications": "Material: Reinforced heavy-gauge tubular steel\nHeight range: 140 cm – 185 cm user height\nMax Load: 130 kg",
                "how_to_use": "Use under supervision of a certified physiotherapist or trained caregiver.",
                "size_guide": "Adjustable for adult heights between 5 ft and 6 ft 2 in.",
            },
            {
                "name": "Deep Tissue Percussion Fascial Massage Gun with 6 Heads",
                "slug": "deep-tissue-percussion-fascial-massage-gun",
                "sku": "OBC-MG-009",
                "category": created_categories["rehabilitation-equipment"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("4500.00"),
                "compare_at_price": Decimal("6000.00"),
                "cost_price": Decimal("2900.00"),
                "stock_quantity": 22,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Rechargeable percussion therapy device with high-torque brushless motor for rapid muscle recovery and myofascial release.",
                "description": "Delivers up to 3200 percussions per minute to penetrate deep into sore muscles, increasing blood flow and breaking up lactic acid knots.",
                "features": "• 30 adjustable speed levels with smart touch LCD\n• 6 interchangeable specialized massage heads\n• 2500mAh lithium-ion battery provides up to 6 hours run time\n• Ultra-quiet motor (<45 dB) with heat dissipation shell",
                "specifications": "Battery: 2500mAh Rechargeable Li-ion\nSpeed Range: 1200 - 3200 RPM\nIncluded: 6 massage heads, Type-C charger, Hard travel case",
                "how_to_use": "Select the desired head attachment, turn on the base switch, and gently glide over muscle groups for 30-60 seconds per zone.",
                "size_guide": "Handheld ergonomic device with carrying case.",
            },
            {
                "name": "TheraBand Resistance Exercise Band Set (5-Level Elastic Loops)",
                "slug": "theraband-resistance-exercise-band-set",
                "sku": "OBC-TB-010",
                "category": created_categories["rehabilitation-equipment"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("2200.00"),
                "compare_at_price": Decimal("2800.00"),
                "cost_price": Decimal("1200.00"),
                "stock_quantity": 40,
                "is_featured": False,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Color-coded progressive latex resistance bands for physiotherapy muscle strengthening and joint range-of-motion drills.",
                "description": "Widely prescribed by Kenyan physical therapists for rotator cuff rehab, knee stabilizer strengthening, glute activation, and post-surgery recovery.",
                "features": "• 5 progressive resistance levels (X-Light, Light, Medium, Heavy, X-Heavy)\n• 100% natural snap-resistant Malaysian latex\n• Includes illustrated workout guide and breathable carry pouch",
                "specifications": "Band Dimensions: 30 cm x 5 cm loop\nResistance: 5 lbs to 40 lbs tension",
                "how_to_use": "Loop around ankles, knees, or wrists for isometric resistance exercises.",
                "size_guide": "Universal set containing 5 resistance levels.",
            },
            {
                "name": "Foldable Bedside Commode Chair with Detachable Bucket",
                "slug": "foldable-bedside-commode-chair",
                "sku": "OBC-CC-011",
                "category": created_categories["home-care"],
                "brand": created_brands["Orthobest Pro"],
                "price": Decimal("6500.00"),
                "compare_at_price": Decimal("7500.00"),
                "cost_price": Decimal("4400.00"),
                "stock_quantity": 14,
                "is_featured": True,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Steel-frame portable commode and over-toilet safety frame with splash guard and removable sanitary bucket.",
                "description": "Multi-purpose 3-in-1 design functions as a standalone bedside commode, a raised toilet seat, and a bathroom safety frame for elderly or mobility-restricted individuals.",
                "features": "• Push-button height-adjustable legs\n• Removable 7-liter commode pail with carry handle and splash-free lid\n• Anti-slip suction rubber feet for wet bathroom safety\n• Quick-fold frame for discreet storage",
                "specifications": "Material: Powder-coated steel & antibacterial molded plastic\nSeat Height: 42 cm – 54 cm adjustable\nWeight Capacity: 120 kg",
                "how_to_use": "Position beside bed for night use or directly over existing toilet bowl as safety frame.",
                "size_guide": "Adjustable height fits standard adult requirements.",
            },
            {
                "name": "Premium Adult Disposable Underpads (Pack of 10 Large Sheets)",
                "slug": "premium-adult-disposable-underpads",
                "sku": "OBC-UP-012",
                "category": created_categories["home-care"],
                "brand": created_brands["CareQuip Medical"],
                "price": Decimal("1200.00"),
                "compare_at_price": Decimal("1500.00"),
                "cost_price": Decimal("750.00"),
                "stock_quantity": 50,
                "is_featured": False,
                "is_bestseller": True,
                "is_new": False,
                "short_description": "Super-absorbent 60x90cm waterproof bed incontinence underpads with diamond quilted polymer core.",
                "description": "High-capacity incontinence protection for hospital beds, mattresses, and wheelchairs. Locks in moisture and neutralizes odors instantly.",
                "features": "• 5-layer absorption core with SAP gel crystals\n• Waterproof polyethylene backing prevents leakage onto bed linens\n• Soft non-woven top sheet gentle on sensitive skin\n• Dimensions: 60 x 90 cm (Extra Large)",
                "specifications": "Absorbency: Up to 1500 ml fluid\nQuantity: 10 underpads per pack",
                "how_to_use": "Lay flat on bed or wheelchair with blue waterproof side facing down and white soft side facing up.",
                "size_guide": "60 cm x 90 cm (Standard Large Hospital Size).",
            },
        ]

        for p_data in products_data:
            prod = Product.objects.create(**p_data)
            # Create default Primary Product Image placeholder
            ProductImage.objects.create(
                product=prod,
                is_primary=True,
                display_order=0,
                alt_text=f"{prod.name} in Kenya"
            )
            # Add sample variants for braces / shoes if applicable
            if "Wrist" in prod.name:
                ProductVariant.objects.create(product=prod, name="Size: Medium (Left Hand)", sku_modifier="-ML", stock_quantity=10)
                ProductVariant.objects.create(product=prod, name="Size: Large (Left Hand)", sku_modifier="-LL", stock_quantity=8)
                ProductVariant.objects.create(product=prod, name="Size: Medium (Right Hand)", sku_modifier="-MR", stock_quantity=12)
                ProductVariant.objects.create(product=prod, name="Size: Large (Right Hand)", sku_modifier="-LR", stock_quantity=10)
            elif "Knee" in prod.name or "Lumbar" in prod.name:
                ProductVariant.objects.create(product=prod, name="Size: Medium", sku_modifier="-M", stock_quantity=10)
                ProductVariant.objects.create(product=prod, name="Size: Large", sku_modifier="-L", stock_quantity=15)
                ProductVariant.objects.create(product=prod, name="Size: XL", sku_modifier="-XL", stock_quantity=8)

            # Add verified customer reviews
            ProductReview.objects.create(
                product=prod,
                customer_name="Dr. Wanjiku M.",
                customer_email="wanjiku.m@gmail.com",
                rating=5,
                title="Excellent clinical quality & fast Nairobi delivery",
                comment=f"Ordered this {prod.name} for a rehabilitation patient in Nairobi. Sturdy build, genuine quality, and arrived in less than 3 hours!",
                verified_purchase=True,
                approved=True
            )
            ProductReview.objects.create(
                product=prod,
                customer_name="Peter Omondi",
                customer_email="omondi.p@yahoo.com",
                rating=5,
                title="Very helpful WhatsApp consultation",
                comment="The team helped me choose the exact right size via WhatsApp before sending the M-Pesa prompt. Highly recommended store.",
                verified_purchase=True,
                approved=True
            )

        # 10. Setup Services
        Service.objects.all().delete()
        services_data = [
            {
                "title": "Orthopedic Brace Fitting & Sizing Guidance",
                "short_summary": "Professional consultation to ensure correct anatomical support, measurements, and maximum rehabilitation comfort.",
                "description": "Our trained specialists assist patients and caregivers in choosing the appropriate brace firmness, hinged mechanisms, and sizing measurements for knees, cervical spine, wrists, and ankles.",
                "icon_name": "activity",
                "display_order": 1,
            },
            {
                "title": "Mobility Aid Customization & Assembly",
                "short_summary": "Tailoring wheelchairs, rollators, and crutches to individual body heights, weights, and daily terrain needs.",
                "description": "We ensure full assembly, brake calibration, cushion positioning, and footrest adjustments before delivery anywhere in Kenya.",
                "icon_name": "wheelchair",
                "display_order": 2,
            },
            {
                "title": "Clinical & Hospital Equipment Procurement",
                "short_summary": "Bulk supply of certified hospital beds, physiotherapy tools, and clinic observation furnishings with wholesale pricing.",
                "description": "We partner with Kenyan medical clinics, nursing homes, and physiotherapy centers for reliable equipment supply, delivery, and warranty support.",
                "icon_name": "heart-pulse",
                "display_order": 3,
            },
            {
                "title": "Homecare & Recovery Support Planning",
                "short_summary": "Equipping family caregivers with patient transfer aids, commode chairs, and anti-bedsore preventative equipment.",
                "description": "Helping families create a safe, hygienic, and dignified recovery environment at home for post-surgical and elderly loved ones.",
                "icon_name": "shield",
                "display_order": 4,
            },
        ]
        for s in services_data:
            Service.objects.create(**s)

        # 11. Setup Blog Posts
        BlogCategory.objects.all().delete()
        BlogPost.objects.all().delete()
        blog_cat1 = BlogCategory.objects.create(name="Rehabilitation Guides")
        blog_cat2 = BlogCategory.objects.create(name="Mobility & Independence")
        blog_cat3 = BlogCategory.objects.create(name="Pain Relief & Ergonomics")

        BlogPost.objects.create(
            title="How to Choose the Right Knee Brace for Ligament & Meniscus Recovery",
            category=blog_cat1,
            author=admin_user,
            excerpt="Understand the critical differences between sleeve compression, hinged stabilizers, and patellar straps to accelerate your knee rehabilitation.",
            content="""<p>Knee injuries such as ACL tears, meniscus damage, and osteoarthritic degradation require specific stabilization mechanisms to prevent reinjury while allowing progressive mobility.</p>
<h3>1. Compression Sleeves vs. Hinged Stabilizers</h3>
<p>While elastic sleeves provide mild warmth and proprioceptive feedback for minor strains, acute ligament instability requires rigid <strong>polycentric dual-hinge braces</strong> that counteract unnatural lateral and medial twisting.</p>
<h3>2. Sizing Accuracy</h3>
<p>Always measure thigh circumference approximately 10 to 15 cm above the mid-kneecap while standing. A brace that is too loose will slip during walking, while an excessively tight fit restricts venous blood return.</p>
<p>Contact our clinical support team at Orthobest Care Hub for personalized sizing verification before ordering.</p>""",
            status='published',
            read_time_minutes=4
        )

        BlogPost.objects.create(
            title="Essential Guide to Buying Wheelchairs in Kenya: Manual vs. Electric",
            category=blog_cat2,
            author=admin_user,
            excerpt="A comprehensive checklist on seat width, frame durability, solid versus pneumatic tires, and transport folding for Kenyan roads.",
            content="""<p>Selecting a wheelchair is a vital decision that impacts daily autonomy, skin integrity, and caregiver ergonomics.</p>
<h3>Key Factors to Evaluate:</h3>
<ul>
<li><strong>Seat Width:</strong> Standard adult chairs measure 18 inches (46 cm). Measure the widest point across the user's hips in a seated position and add 2 to 3 cm of clearance.</li>
<li><strong>Tire Type:</strong> For Kenyan outdoor pavements and suburban paths, solid puncture-proof polyurethane tires eliminate flat-tire inconveniences.</li>
<li><strong>Weight & Portability:</strong> Ensure the folding mechanism allows easy storage in standard vehicle trunks or Matatus.</li>
</ul>""",
            status='published',
            read_time_minutes=5
        )

        BlogPost.objects.create(
            title="5 Practical Ways to Relieve Lower Back Pain at Work and Home",
            category=blog_cat3,
            author=admin_user,
            excerpt="Discover how ergonomic lumbar sacral belts, proper workstation seating, and gentle stretching alleviate sciatica and disc strain.",
            content="""<p>Lower back discomfort is among the leading causes of workplace absenteeism in Kenya. Prolonged sitting exerts immense pressure on the lumbar discs (L4-L5 and L5-S1).</p>
<h3>Effective Strategies:</h3>
<ol>
<li>Use a dual-pull lumbar sacral support belt during prolonged standing or lifting tasks.</li>
<li>Ensure your knees remain at a 90-degree angle with feet flat on the floor while working at your desk.</li>
<li>Incorporate mini-breaks every 45 minutes to stretch hip flexors and decompress the spine.</li>
</ol>""",
            status='published',
            read_time_minutes=3
        )

        # 12. Setup FAQs
        FAQ.objects.all().delete()
        faqs_data = [
            {"category": "Orders & Delivery", "question": "How fast is delivery within Nairobi and across Kenya?", "answer": "Within Nairobi CBD and surrounding suburbs, orders are delivered within 2 to 4 hours via rider dispatch. Upcountry deliveries to Mombasa, Kisumu, Nakuru, Eldoret, and all 47 counties arrive within 24 to 48 hours via established courier partners (Fargo Courier, G4S, or direct coach parcel services).", "display_order": 1},
            {"category": "Payments & M-Pesa", "question": "What payment methods do you accept?", "answer": "We accept Safaricom M-Pesa via automated STK Push, Paybill, and Till transfer. We also offer Pay on Delivery (Cash or M-Pesa on arrival) for deliveries within Nairobi and select nearby counties.", "display_order": 2},
            {"category": "Products & Sizing", "question": "How do I choose the correct size for a knee brace or lumbar belt?", "answer": "Each product page contains a detailed measurement guide. If you are uncertain, simply click the 'Chat on WhatsApp' button on the product page or call 0798 246 811. Our team will guide you on taking accurate tape measurements.", "display_order": 3},
            {"category": "General", "question": "Where is Orthobest Care Hub physically located in Nairobi?", "answer": "Our store and clinical showroom is situated in Nairobi CBD on Mfangano Street, Travis Building, 3rd Floor, Room C37, Wing C (Adjacent to Quickmart Supermarket). We are open Monday to Friday 9 AM to 5 PM and Saturday 9 AM to 3 PM.", "display_order": 4},
            {"category": "Products & Sizing", "question": "Are your medical products certified and genuine?", "answer": "Yes, 100%. All orthopedic supports, mobility aids, hospital beds, and rehabilitation appliances supplied by Orthobest Care Hub meet strict medical manufacturing and quality compliance standards.", "display_order": 5},
            {"category": "Orders & Delivery", "question": "Can I return or exchange an item if it doesn't fit?", "answer": "Yes! Unused products with original packaging and tags can be exchanged within 7 days of delivery. Please contact our support team immediately to arrange an exchange.", "display_order": 6},
        ]
        for f in faqs_data:
            FAQ.objects.create(**f)

        # 13. Setup Legal Pages
        LegalPage.objects.all().delete()
        LegalPage.objects.create(
            slug="privacy-policy",
            title="Privacy Policy",
            content="""<h2>Orthobest Care Hub Privacy Commitment</h2>
<p>At Orthobest Care Hub (orthobestcarehub.co.ke), protecting your personal information and health-commerce confidentiality is of paramount importance. This Privacy Policy details how we collect, handle, and protect your information.</p>
<h3>1. Information We Collect</h3>
<p>We collect details you provide during order placement, checkout, or inquiry, including your name, delivery address, phone number, email address, and order history.</p>
<h3>2. Use of Information</h3>
<p>Your details are used strictly to fulfill product orders, dispatch deliveries across Kenya, provide order status notifications via SMS/email, and assist you with sizing advice.</p>
<h3>3. Payment Security</h3>
<p>We never store your M-Pesa PIN or credit card numbers. All electronic payments are processed through encrypted channels provided by licensed Kenyan financial gateways.</p>
<h3>4. Contact</h3>
<p>For any data protection inquiries, email us at <strong>info@orthobestcarehub.co.ke</strong>.</p>"""
        )

        LegalPage.objects.create(
            slug="terms-conditions",
            title="Terms & Conditions",
            content="""<h2>Terms of Service</h2>
<p>By accessing or placing an order on Orthobest Care Hub (orthobestcarehub.co.ke), you agree to be bound by these terms and conditions.</p>
<h3>1. Product Descriptions & Pricing</h3>
<p>All prices are listed in Kenyan Shillings (KSh / KES) and are inclusive of relevant statutory taxes where applicable. We endeavor to display accurate pricing and stock availability.</p>
<h3>2. Medical Advice Disclaimer</h3>
<p>Content published on this website is for general informational purposes only. It is not intended to substitute professional medical diagnosis or personalized healthcare consultation.</p>
<h3>3. Order Confirmation & Fulfillment</h3>
<p>An order is confirmed upon receipt of valid payment or confirmation of Pay on Delivery approval by our dispatch operations team.</p>"""
        )

        LegalPage.objects.create(
            slug="shipping-policy",
            title="Shipping & Delivery Policy",
            content="""<h2>Delivery Across Kenya</h2>
<p>Orthobest Care Hub operates a fast, secure delivery network covering Nairobi and all 47 counties in Kenya.</p>
<h3>Delivery Rates & Timelines:</h3>
<ul>
<li><strong>Nairobi CBD:</strong> KSh 200 (Delivery within 2 - 4 Hours)</li>
<li><strong>Nairobi Suburbs (Westlands, Karen, Kilimani, Kasarani, etc.):</strong> KSh 300 (Same Day Delivery)</li>
<li><strong>Kiambu & Machakos (Thika, Ruiru, Kikuyu, Athi River):</strong> KSh 450 (Same Day / Next Day)</li>
<li><strong>Upcountry Kenya (Mombasa, Kisumu, Nakuru, Eldoret, etc.):</strong> KSh 600 (24 - 48 Hours via Fargo Courier / G4S / Doorstep Delivery)</li>
</ul>"""
        )

        LegalPage.objects.create(
            slug="returns-refund-policy",
            title="Returns & Refund Policy",
            content="""<h2>7-Day Return & Exchange Policy</h2>
<p>Your satisfaction with rehabilitation comfort is our goal. If an item does not fit or arrives defective, we are here to help.</p>
<h3>1. Eligibility for Returns:</h3>
<ul>
<li>Items must be in brand new, unused condition with all original packaging, tags, and manuals intact.</li>
<li>Return requests must be initiated within 7 calendar days of receipt.</li>
<li>Hygiene items (such as opened disposable underpads) cannot be returned once unsealed.</li>
</ul>
<h3>2. How to Request an Exchange:</h3>
<p>WhatsApp our support line at <strong>+254 798 246 811</strong> or email <strong>info@orthobestcarehub.co.ke</strong> with your order number.</p>"""
        )

        self.stdout.write(self.style.SUCCESS("Orthobest Care Hub database populated successfully with audited Kenyan data!"))
