# MASTER AI CODING AGENT PROMPT

* MAKE SURE it is a Gen-Z-style storefront, including product search, filters, categories, cart, checkout, customer accounts, order tracking, WhatsApp CTA, responsive mobile design, and an administrative dashboard.

# ORTHOBEST CARE HUB — COMPLETE DJANGO E-COMMERCE REDEVELOPMENT

## PROJECT TYPE

You are a senior full-stack Django engineer, UI/UX designer, e-commerce architect, SEO specialist, security engineer, and DevOps engineer.

You are going to completely redevelop an existing Kenyan orthopedic, rehabilitation, medical-support-products, and healthcare e-commerce website.

### CURRENT WEBSITE

Existing website:

`https://orthobestcarerehab.co.ke/`

### NEW BRAND / DOMAIN

The owner wants to move to:

`https://orthobestcarehub.co.ke/`

### CORE REQUIREMENT

Build a **completely modern, premium, mobile-first, Gen-Z-friendly, conversion-focused e-commerce website** for Orthobest Care Hub.

The new website must not feel like an ordinary WordPress/template-based medical website.

It should feel like a modern Kenyan health-commerce startup combining:

* Healthcare credibility
* Medical-product professionalism
* Modern e-commerce
* Gen-Z visual design
* Mobile-first shopping
* Fast product discovery
* Easy checkout
* WhatsApp communication
* M-Pesa-friendly Kenyan purchasing
* Strong SEO
* Excellent accessibility
* Trust and credibility
* Professional healthcare branding

The Products section could support things such as:
Orthopedic Products
Medical Equipment
Mobility Aids
Wheelchairs
Walking Aids
Braces & Supports
Rehabilitation Equipment
Homecare Products

with:
Product
├── name
├── category
├── description
├── price
├── discount_price
├── stock_quantity
├── main_image
├── additional_images
├── brand
├── SKU
├── featured
├── available
├── created_at
└── updated_at

IMPORTANT:

The existing website is the business reference source.

Before replacing anything, perform a comprehensive audit of the existing website if internet access is available.

Do NOT blindly invent products, prices, services, contact information, addresses, medical claims, certifications, brands, or business information.

Where existing website information is accessible, migrate/preserve the information.

Where information is unavailable, create the appropriate Django admin fields/placeholders so the owner can populate them later.

---

# 1. NON-NEGOTIABLE TECHNOLOGY REQUIREMENTS

## Backend

Use:

* Python
* Django
* Django Templates
* Django ORM
* PostgreSQL
* Django Admin
* Django authentication
* Django forms
* Django messages
* Django sessions
* Django email framework

DO NOT use:

* React
* Next.js
* Vue
* Angular
* Laravel
* Node.js backend
* WordPress
* Shopify
* WooCommerce

The entire application must be Django-based.

Frontend JavaScript is allowed only where necessary for interactive functionality.

Use modern HTML5, CSS3 and vanilla JavaScript.

You may use lightweight frontend libraries only when genuinely useful, but avoid unnecessary dependencies.

---

# 2. PROJECT ARCHITECTURE

Create a clean modular Django project.

Suggested structure:

```text
orthobestcarehub/
│
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/
│   ├── products/
│   ├── categories/
│   ├── cart/
│   ├── orders/
│   ├── payments/
│   ├── customers/
│   ├── accounts/
│   ├── reviews/
│   ├── wishlist/
│   ├── blog/
│   ├── contact/
│   ├── newsletter/
│   └── search/
│
├── templates/
├── static/
├── media/
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

You may adjust the structure if a better Django architecture is appropriate.

Do NOT unnecessarily split functionality into dozens of tiny apps.

Keep the code maintainable.

---

# 3. FIRST TASK — AUDIT THE EXISTING WEBSITE

Before implementation, inspect:

`https://orthobestcarerehab.co.ke/`

Attempt to identify ALL publicly accessible:

* Homepage
* About page
* Contact page
* Product pages
* Product categories
* Services
* Shopping cart
* Checkout
* Payment process
* Customer/account pages
* Blog/articles
* FAQs
* Policies
* Shipping information
* Returns/refund information
* Privacy policy
* Terms and conditions
* Footer links
* Header navigation
* WhatsApp links
* Phone numbers
* Email addresses
* Social media links
* Product images
* Product names
* Product descriptions
* Prices
* Product variants
* Stock information
* Brands
* Product categories
* Product attributes
* Existing URLs/slugs

If the old website exposes an e-commerce checkout/payment workflow, reproduce the BUSINESS LOGIC but modernize the UX.

Do not copy outdated design.

Do not remove useful functionality simply because the new design is different.

---

# 4. BRAND TRANSITION

The old brand/domain is:

Orthobest Care Rehab

The new brand should be:

# Orthobest Care Hub

New domain:

`orthobestcarehub.co.ke`

The architecture must be prepared for domain migration.

Use environment variables:

```env
SITE_NAME=Orthobest Care Hub
SITE_DOMAIN=orthobestcarehub.co.ke
OLD_DOMAIN=orthobestcarerehab.co.ke
```

Implement SEO-friendly permanent redirects from old URLs to corresponding new URLs where possible.

Do not simply redirect every old URL to the homepage.

Create a URL migration map.

Example:

```text
old-domain/product/example-product/
        ↓
new-domain/products/example-product/
```

Preserve SEO equity wherever possible.

---

# 5. DESIGN DIRECTION

The website must look like a **premium modern health-commerce platform**.

Avoid:

* Old-fashioned hospital website appearance
* Excessive blue medical templates
* Generic Bootstrap-looking layouts
* Huge walls of text
* Cluttered product pages
* Tiny typography
* Poor mobile layouts
* Excessive gradients
* Cheap-looking stock graphics
* Overloaded animations
* Autoplay video
* Slow hero sliders
* Excessive shadows
* Outdated e-commerce layouts

Instead use:

* Clean whitespace
* Large typography
* Modern cards
* Rounded but professional UI
* Strong visual hierarchy
* High-quality product photography
* Crisp icons
* Subtle animations
* Sticky mobile navigation
* Modern search
* Clear CTAs
* Product badges
* Trust indicators
* Clean checkout
* Excellent mobile UX

The design should feel contemporary in 2026.

---

# 6. TARGET USERS

Design primarily for:

* Kenyan consumers
* Patients
* Caregivers
* People recovering from injuries
* People requiring orthopedic support
* Physiotherapy patients
* Elderly customers
* People with mobility needs
* Sports/injury-recovery customers
* Hospitals
* Clinics
* Physiotherapists
* Medical professionals
* Care institutions
* Home-care customers

The interface must remain accessible to older and less tech-savvy users despite having a Gen-Z visual style.

Do NOT sacrifice usability for aesthetics.

---

# 7. MOBILE-FIRST REQUIREMENT

This is extremely important.

The website must be designed mobile-first.

Primary experience:

Mobile phone.

Test at minimum:

* 320px
* 360px
* 375px
* 390px
* 414px
* 430px
* 768px
* 1024px
* 1280px
* 1440px
* 1920px

No:

* horizontal scrolling
* broken grids
* overflowing text
* tiny buttons
* unusable dropdowns
* overlapping cards
* broken images
* desktop-only checkout

Mobile navigation must be excellent.

---

# 8. GLOBAL HEADER

Create a modern header.

Desktop:

```text
[LOGO]   Shop   Categories   Services   About   Resources   Contact

             [Search] [Account] [Wishlist] [Cart]
```

Mobile:

```text
[☰] [LOGO]                  [Search] [Cart]
```

The header should support:

* Sticky positioning
* Search
* Account
* Wishlist
* Cart
* Mobile menu
* Category navigation

Use a clean mega-menu where appropriate.

---

# 9. TOP ANNOUNCEMENT BAR

Create an optional configurable announcement bar.

Examples:

```text
🚚 Fast Delivery Across Kenya
```

or:

```text
🛍️ Shop Orthopedic & Rehabilitation Products Online
```

or:

```text
💬 Need Help Choosing a Product? Chat With Us
```

The text must be editable from Django Admin.

Allow the admin to enable/disable it.

---

# 10. HOMEPAGE

Create a highly polished homepage.

Recommended structure:

## Section 1 — Hero

Large modern hero section.

Headline should communicate the value proposition.

Example concept:

> SUPPORT YOUR MOVEMENT.
> LIVE WITH CONFIDENCE.

Supporting copy:

> Quality orthopedic, rehabilitation and mobility solutions designed to support recovery, comfort and everyday independence.

Primary CTA:

`SHOP PRODUCTS`

Secondary CTA:

`TALK TO A SPECIALIST`

Hero should include a professionally presented healthcare/product image.

Do not invent medical claims.

Hero content must be editable from Django Admin.

---

# 11. TRUST STRIP

Immediately below hero.

Example:

```text
✓ Quality Products
✓ Trusted Healthcare Solutions
✓ Delivery Across Kenya
✓ Customer Support
✓ Secure Checkout
```

Make these configurable.

---

# 12. PRODUCT CATEGORY SECTION

Display major categories as visual cards.

Possible categories may include:

* Orthopedic Supports
* Rehabilitation Equipment
* Mobility Aids
* Physiotherapy Products
* Compression Products
* Braces & Supports
* Wheelchairs
* Walking Aids
* Medical Equipment
* Daily Living Aids
* Home Care
* Sports Recovery

IMPORTANT:

Only use categories that exist in the real business or that the owner approves.

Categories must be manageable through Django Admin.

Each category should have:

* Name
* Slug
* Description
* Image
* Icon
* Featured status
* Display order
* SEO title
* SEO description

---

# 13. FEATURED PRODUCTS

Create a modern product carousel/grid.

Each card should show:

* Product image
* Product name
* Price
* Previous price if applicable
* Discount badge
* Stock badge
* Category
* Rating
* Wishlist button
* Quick view
* Add to cart

Example:

```text
[PRODUCT IMAGE]

BEST SELLER

Knee Support Brace
★★★★☆ (12)

KSh 2,500

[Add to Cart]
```

Use Kenyan currency:

# KSh

Prices must come from the database.

Never hardcode product prices.

---

# 14. PRODUCT SYSTEM

Create a robust product model.

Suggested fields:

```text
Product
-------
name
slug
sku
short_description
description
category
brand
price
compare_at_price
cost_price
stock_quantity
low_stock_threshold
is_available
is_featured
is_bestseller
is_new
is_on_sale
weight
dimensions
meta_title
meta_description
created_at
updated_at
```

Add product images through a separate model:

```text
ProductImage
------------
product
image
alt_text
caption
display_order
is_primary
```

Support multiple images per product.

---

# 15. PRODUCT ATTRIBUTES

Some medical/orthopedic products may have variants.

Support:

* Size
* Colour
* Side
* Model
* Capacity
* Material
* Other custom attributes

Do not hardcode these attributes.

Create a flexible attribute/variant system.

Example:

```text
Knee Brace
Size: S / M / L / XL
Side: Left / Right
```

Price and stock can optionally differ by variant.

---

# 16. PRODUCT DETAIL PAGE

This is one of the most important pages.

Create a premium e-commerce product page.

Desktop:

```text
------------------------------------------------
IMAGE GALLERY       PRODUCT INFORMATION
------------------------------------------------
                     Product Name
                     ★★★★★
                     SKU

                     KSh 4,500
                     Was KSh 5,500

                     Short description

                     Size:
                     [S] [M] [L] [XL]

                     Quantity [- 1 +]

                     [ADD TO CART]
                     [BUY NOW]

                     ♡ Add to Wishlist

                     🚚 Delivery across Kenya
                     🔒 Secure checkout
                     💬 Need help? WhatsApp us
------------------------------------------------
```

Below:

Tabs/sections:

* Description
* Features
* Specifications
* How to Use
* Size Guide
* Shipping
* Returns
* Reviews
* FAQs

Only show sections where information exists.

---

# 17. MEDICAL PRODUCT DISCLAIMER

Because this is a healthcare-related store, do NOT make unsupported medical claims.

Where appropriate, display a professional disclaimer such as:

> Product information is provided for general informational purposes and does not replace professional medical advice. Consult a qualified healthcare professional when unsure which product is appropriate for your needs.

Make this configurable through admin.

Do not claim that a product:

* cures a disease
* guarantees recovery
* replaces medical treatment
* prevents a medical condition

unless the business has legitimate evidence and the owner explicitly provides approved wording.

---

# 18. PRODUCT SEARCH

Build a powerful search system.

Search should support:

* Product name
* SKU
* Category
* Brand
* Keywords
* Description

Search UI:

```text
What are you looking for?

[ 🔍 Search orthopedic supports, wheelchairs, braces... ]
```

Show live suggestions where practical.

Search results should display:

* Product image
* Product name
* Price
* Category
* Availability
* Add to cart

Provide:

```text
Search results for "knee brace"
```

---

# 19. PRODUCT FILTERING

Category/product listing pages must support:

* Category
* Price range
* Brand
* Availability
* Size
* Product type
* Rating
* New arrivals
* Best sellers
* Sale

Mobile filtering should open as a bottom sheet/modal.

Desktop filtering can be sidebar-based.

---

# 20. PRODUCT SORTING

Provide:

* Featured
* Newest
* Price: Low → High
* Price: High → Low
* Best Selling
* Highest Rated
* Name A → Z

---

# 21. SHOP PAGE

Create:

`/shop/`

Include:

* Hero/banner
* Categories
* Filters
* Search
* Sorting
* Product grid
* Pagination

Do NOT load hundreds of products at once.

Use pagination.

---

# 22. CATEGORY PAGES

Create SEO-friendly URLs:

```text
/shop/
 /category/orthopedic-supports/
 /category/mobility-aids/
 /category/rehabilitation-equipment/
```

Category page should include:

* Category title
* Description
* Category image
* Product count
* Filters
* Sorting
* Products
* FAQ
* SEO content

---

# 23. SHOPPING CART

Create a professional cart.

Cart must work for guest users.

Use Django sessions for guest carts.

Authenticated users should have persistent carts where practical.

Cart should show:

```text
YOUR CART

Product             Qty        Price

[Image] Knee Brace   - 1 +     KSh 2,500

Subtotal                         KSh 2,500
Delivery                         KSh 300
-----------------------------------------
TOTAL                            KSh 2,800

[PROCEED TO CHECKOUT]
```

Allow:

* Quantity update
* Remove product
* Save for later
* Wishlist
* Continue shopping

Automatically update totals.

Use AJAX/fetch where appropriate.

Do not require full page reload for simple cart quantity updates.

---

# 24. MINI CART

Add a mini-cart drawer.

When user adds product:

```text
✓ Added to cart

Knee Support Brace
KSh 2,500

[View Cart] [Checkout]
```

Do not use intrusive alerts.

---

# 25. WISHLIST

Create wishlist functionality.

Authenticated users:

* Persistent wishlist

Guests:

* Session-based wishlist if practical

Features:

* Add/remove
* Move to cart
* Product availability indicator

---

# 26. CHECKOUT

The checkout experience must be extremely simple.

Do not create a complicated multi-page checkout.

Prefer a streamlined checkout.

Fields:

## Customer

* First name
* Last name
* Email
* Phone number

## Delivery

* County
* Town/City
* Estate/Area
* Building/House
* Delivery notes

## Order

* Cart summary
* Delivery fee
* Discount
* Total

## Payment

Display available payment methods.

Potential methods:

* M-Pesa
* Card
* Pay on Delivery if business policy allows
* Manual payment if required

Do NOT activate payment methods that the business has not approved.

---

# 27. KENYAN PAYMENT EXPERIENCE

The website is targeting Kenya.

Therefore design the checkout around Kenyan customers.

Currency:

`KES / KSh`

Phone number should support:

```text
+254
07...
01...
```

Normalize phone numbers internally.

For M-Pesa integration, build the architecture so the payment provider can be configured via environment variables.

Do not hardcode API credentials.

Example:

```env
MPESA_CONSUMER_KEY=
MPESA_CONSUMER_SECRET=
MPESA_PASSKEY=
MPESA_SHORTCODE=
MPESA_CALLBACK_URL=
```

Use a payment service abstraction.

Example:

```python
PaymentGateway
    ├── MpesaGateway
    ├── CardGateway
    └── ManualPaymentGateway
```

This allows the business to change providers later.

---

# 28. PAYMENT STATUS

Create proper payment states:

```text
PENDING
PROCESSING
SUCCESS
FAILED
CANCELLED
REFUNDED
```

Never mark an order as paid simply because the customer reached the success page.

Payment confirmation must be based on the verified provider response/callback.

Log payment transactions.

Never store raw card information.

---

# 29. ORDER SYSTEM

Create robust models.

Suggested:

```text
Order
-----
order_number
customer
email
phone
status
payment_status
subtotal
delivery_fee
discount
total
currency
shipping_address
notes
created_at
updated_at
```

Order item:

```text
OrderItem
---------
order
product
product_name
sku
unit_price
quantity
total
```

IMPORTANT:

Store the product name and price at the time of purchase.

Do not depend entirely on the current product price.

If product price later changes, old orders must remain historically correct.

---

# 30. ORDER STATUS

Support:

```text
Pending
Confirmed
Processing
Ready for Dispatch
Shipped
Delivered
Cancelled
Returned
Refunded
```

Admin must be able to update status.

Customers should see order status.

---

# 31. ORDER CONFIRMATION

After checkout:

Show:

```text
ORDER CONFIRMED 🎉

Thank you for your order.

Order #: OBC-2026-000123

We'll contact you using:
+254...

[VIEW ORDER]
[CONTINUE SHOPPING]
```

Send confirmation email where email is provided.

Prepare architecture for WhatsApp/SMS notifications.

---

# 32. CUSTOMER ACCOUNT

Create:

`/account/`

Dashboard:

```text
Hello, Customer 👋

Orders
Wishlist
Addresses
Profile
Account Settings
Logout
```

Orders page:

* Order number
* Date
* Total
* Status
* Payment status
* View order

Order detail:

* Products
* Quantities
* Price
* Delivery information
* Payment
* Status timeline

---

# 33. GUEST CHECKOUT

Do NOT force account creation.

Allow guest checkout.

After order completion:

Offer:

```text
Want to track future orders faster?

[Create an Account]
```

---

# 34. WHATSAPP INTEGRATION

This is important for the Kenyan market.

Add floating WhatsApp CTA.

Possible text:

```text
Need help choosing a product?
Chat with us on WhatsApp.
```

Product pages should have:

```text
💬 Ask about this product
```

Clicking it should generate a WhatsApp message containing product name.

Example concept:

```text
Hello Orthobest Care Hub, I am interested in the [PRODUCT NAME]. Please assist me.
```

The WhatsApp number must be configurable through Django Admin/settings.

Do not hardcode it in templates.

---

# 35. CONTACT PAGE

Create a professional contact page.

Include:

* Phone
* WhatsApp
* Email
* Physical location
* Opening hours
* Google Maps
* Contact form
* Social links

All business information should be editable through Django Admin.

---

# 36. ABOUT PAGE

Create a modern About page.

Sections:

* Who We Are
* What We Do
* Our Mission
* Our Vision
* Why Choose Us
* Quality & Trust
* Customer-first approach

Do not invent company history.

Use existing website information where available.

---

# 37. SERVICES

If the existing business offers services beyond product sales, preserve them.

Possible structure:

```text
Services

Orthopedic Support
Rehabilitation
Mobility Support
Physiotherapy Products
Home Care
Product Guidance
```

Only use services confirmed by the owner.

---

# 38. BLOG / RESOURCES

Create a modern content system.

URL:

```text
/blog/
```

Articles:

```text
/blog/article-slug/
```

Admin should manage:

* Title
* Slug
* Featured image
* Author
* Content
* Excerpt
* Category
* Tags
* SEO title
* SEO description
* Published date
* Published status

Content examples can include educational topics such as:

* How to choose a knee brace
* Wheelchair buying guide
* Mobility aid selection
* Rehabilitation equipment guide
* Compression support guide

IMPORTANT:

Educational content must not make unsafe medical claims.

---

# 39. FAQ SYSTEM

Create:

`/faq/`

Admin-managed FAQs.

Support:

* Question
* Answer
* Category
* Display order
* Active status

Add FAQ schema where valid.

---

# 40. REVIEWS

Create customer reviews.

Fields:

```text
product
customer
rating
title
comment
verified_purchase
approved
created_at
```

Only display approved reviews.

Admin moderation required.

Prevent obvious spam.

---

# 41. NEWSLETTER

Create newsletter subscription.

Fields:

```text
email
name
subscribed
created_at
```

Add footer subscription form.

Implement basic validation.

Never expose subscriber emails publicly.

---

# 42. SEO

SEO must be built into the architecture.

Every major page should support:

* SEO title
* Meta description
* Canonical URL
* Open Graph title
* Open Graph description
* Open Graph image
* Twitter/X card
* Structured data where appropriate

Product schema should include valid:

* Product name
* Image
* Description
* SKU
* Price
* Currency
* Availability
* Aggregate rating where legitimate

Do not fabricate ratings.

---

# 43. URL STRUCTURE

Use clean URLs.

Examples:

```text
/
 /shop/
 /category/<slug>/
 /product/<slug>/
 /cart/
 /checkout/
 /order/success/
 /account/
 /wishlist/
 /about/
 /services/
 /contact/
 /blog/
 /blog/<slug>/
 /faq/
 /privacy-policy/
 /terms/
 /shipping-policy/
 /returns-policy/
```

Avoid URLs like:

```text
/product.php?id=123
```

---

# 44. SEO MIGRATION

Create a migration plan from:

`orthobestcarerehab.co.ke`

to:

`orthobestcarehub.co.ke`

Implement:

* 301 redirects
* Canonical URLs
* Sitemap
* Robots.txt
* Correct metadata
* Google Search Console readiness
* Structured data
* Preservation of useful old URLs

Do not create redirect chains.

---

# 45. SITEMAP

Implement Django sitemap framework.

Include:

* Products
* Categories
* Pages
* Blog posts

Exclude:

* Cart
* Checkout
* Account
* Login
* Admin
* Internal search results

---

# 46. ROBOTS.TXT

Create a proper robots.txt.

Allow public content.

Disallow:

```text
/admin/
 /account/
 /cart/
 /checkout/
```

Do not accidentally block product/category pages.

---

# 47. PERFORMANCE

Performance is critical.

Optimize:

* Images
* CSS
* JavaScript
* Database queries
* Product listing
* Search
* Fonts
* Lazy loading

Use:

```html
loading="lazy"
```

where appropriate.

Use responsive image sizes.

Avoid loading huge original images unnecessarily.

---

# 48. DATABASE OPTIMIZATION

Use:

```python
select_related()
prefetch_related()
```

where appropriate.

Add database indexes for:

* slug
* SKU
* category
* price
* availability
* created_at
* order number
* payment reference

Avoid N+1 queries.

---

# 49. CACHING

Prepare the system for caching.

Potential cache targets:

* Homepage sections
* Categories
* Product listings
* Navigation
* Frequently accessed content

Do not cache user-specific information incorrectly.

---

# 50. SECURITY

Follow Django security best practices.

Implement:

* CSRF protection
* XSS protection
* Secure cookies
* HTTPS-ready configuration
* Password hashing
* Session security
* Authentication protections
* Permission checks
* Admin protection
* File upload validation
* Image validation
* Input validation
* Rate limiting where appropriate

Never expose:

* SECRET_KEY
* database credentials
* payment credentials
* API keys

---

# 51. ENVIRONMENT VARIABLES

Create `.env.example`.

Example:

```env
DEBUG=False

SECRET_KEY=

ALLOWED_HOSTS=

DATABASE_URL=

SITE_NAME=Orthobest Care Hub
SITE_DOMAIN=orthobestcarehub.co.ke

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True

MPESA_CONSUMER_KEY=
MPESA_CONSUMER_SECRET=
MPESA_PASSKEY=
MPESA_SHORTCODE=
MPESA_CALLBACK_URL=

WHATSAPP_NUMBER=

GOOGLE_MAPS_API_KEY=
```

Never commit `.env`.

---

# 52. DJANGO ADMIN

The admin panel must be excellent.

Register and customize:

* Products
* Product images
* Categories
* Brands
* Product variants
* Orders
* Order items
* Payments
* Customers
* Reviews
* Blog posts
* FAQs
* Newsletter subscribers
* Pages
* Site settings
* Homepage sections
* Coupons
* Delivery zones

Use:

* search_fields
* list_display
* list_filter
* prepopulated_fields
* autocomplete_fields
* inline models
* date_hierarchy
* fieldsets

where useful.

---

# 53. ADMIN DASHBOARD

Create a useful business dashboard.

Show:

```text
Today's Sales
Orders Today
Pending Orders
Products Low in Stock
Customers
Revenue
Top Products
Recent Orders
```

Charts may include:

* Sales over time
* Orders over time
* Top-selling products
* Revenue by category

Keep it clean and useful.

---

# 54. INVENTORY

Inventory must be database-driven.

Features:

* Stock quantity
* Low-stock threshold
* Out-of-stock status
* Backorder option
* Stock adjustment
* Inventory history

When an order is successfully confirmed, inventory should be handled correctly.

Prevent overselling.

---

# 55. COUPONS / DISCOUNTS

Prepare a coupon system.

Fields:

```text
code
discount_type
discount_value
minimum_order
maximum_discount
start_date
end_date
usage_limit
active
```

Support:

* Percentage discount
* Fixed KSh discount

Validate coupons server-side.

---

# 56. DELIVERY

Create configurable delivery zones.

Example:

```text
Nairobi
Kiambu
Machakos
Mombasa
Kisumu
Nakuru
Other Kenya
```

Do not hardcode delivery prices.

Admin must configure:

```text
Zone
Delivery fee
Estimated delivery time
Active
```

Checkout calculates delivery based on selected location.

---

# 57. CONTACT/LEAD MANAGEMENT

Contact form submissions should be stored.

Model:

```text
ContactMessage
--------------
name
email
phone
subject
message
created_at
status
```

Admin can mark:

```text
New
In Progress
Resolved
```

---

# 58. DESIGN SYSTEM

Create reusable design tokens.

Example:

```css
:root {
    --primary: ...;
    --secondary: ...;
    --accent: ...;
    --background: ...;
    --surface: ...;
    --text: ...;
    --muted: ...;
    --border: ...;
    --success: ...;
    --danger: ...;
}
```

Do not randomly use colors throughout templates.

Use a coherent design system.

The final colors should be based on the actual Orthobest Care Hub branding/logo.

If no official palette is available, create a professional healthcare/e-commerce palette and make it easy to change centrally.

---

# 59. TYPOGRAPHY

Use a modern highly readable font system.

Prioritize:

* readability
* accessibility
* performance

Typography hierarchy:

```text
Hero heading
H1
H2
H3
Body
Small text
Labels
Buttons
```

Avoid excessively thin fonts.

---

# 60. MICRO-INTERACTIONS

Use subtle modern interactions:

* Button hover
* Card hover
* Image zoom
* Wishlist animation
* Cart drawer
* Toast notification
* Smooth accordion
* Skeleton loading where useful
* Filter transitions

Do not over-animate the website.

Respect:

```css
prefers-reduced-motion
```

---

# 61. ACCESSIBILITY

Target WCAG-conscious implementation.

Include:

* Semantic HTML
* Proper labels
* Keyboard navigation
* Focus states
* Alt text
* Sufficient contrast
* Accessible forms
* Accessible modals
* Accessible menus
* ARIA only where necessary

Do not rely only on color to communicate status.

---

# 62. ERROR PAGES

Create beautiful custom:

* 404
* 403
* 500

pages.

Maintain the site's branding.

404 example:

```text
Oops — this page moved.

Let's get you back to the products you need.

[GO TO SHOP]
```

---

# 63. LOADING STATES

Implement polished loading states where AJAX is used.

Do not allow buttons to appear frozen.

Example:

```text
Adding...
```

instead of:

```text
Add to Cart
```

while the request is processing.

Prevent duplicate submissions.

---

# 64. FORMS

All forms must have:

* CSRF
* Validation
* Error messages
* Success messages
* Accessible labels
* Proper input types

Use Django Forms or ModelForms.

Do not trust client-side validation alone.

---

# 65. ADMIN CONTENT MANAGEMENT

The owner should be able to change without developer intervention:

* Homepage hero
* Announcement bar
* Categories
* Products
* Prices
* Stock
* Product images
* Product descriptions
* Homepage featured products
* Services
* FAQs
* Blog posts
* Contact information
* Social media links
* Delivery charges
* Store policies
* SEO metadata

Avoid hardcoding business content.

---

# 66. HOMEPAGE CONTENT MANAGEMENT

Create configurable sections.

Possible sections:

```text
Announcement
Hero
Trust indicators
Featured categories
Featured products
Best sellers
Promo banner
Why choose us
Services
Educational content
Testimonials
Newsletter
CTA
```

Admin can:

* Enable/disable section
* Change title
* Change text
* Change image
* Change button
* Change order

---

# 67. SOCIAL MEDIA

Create configurable social links.

Potential:

* Facebook
* Instagram
* TikTok
* WhatsApp
* YouTube
* X

Only display platforms where the business has an official account.

---

# 68. ANALYTICS READINESS

Prepare for:

* Google Analytics
* Google Tag Manager
* Meta Pixel
* Conversion tracking

Do not hardcode tracking IDs.

Use environment variables or Django settings.

Track important e-commerce events where possible:

* Product view
* Add to cart
* Begin checkout
* Purchase
* Search
* Wishlist

---

# 69. EMAIL SYSTEM

Prepare transactional email templates:

* Order confirmation
* Payment confirmation
* Order status update
* Password reset
* Contact form notification

Use HTML email templates.

Keep email branding consistent.

---

# 70. WHATSAPP ORDER SUPPORT

Provide WhatsApp CTA after purchase:

```text
Need help with your order?

[CHAT ON WHATSAPP]
```

The generated message should contain the order number.

---

# 71. LEGAL PAGES

Create editable pages:

* Privacy Policy
* Terms & Conditions
* Shipping Policy
* Returns & Refund Policy
* Cookie Policy

Do not invent legally binding business-specific terms.

Use placeholders where owner/legal review is required.

---

# 72. COOKIE / PRIVACY

If analytics/marketing cookies are implemented, prepare an appropriate cookie consent mechanism.

Do not secretly install unnecessary tracking.

---

# 73. PRODUCT IMAGE HANDLING

Product images must:

* Be optimized
* Have alt text
* Support multiple images
* Have thumbnails
* Maintain aspect ratios
* Avoid layout shifts

Use appropriate image processing if needed.

---

# 74. DATA MIGRATION

Create a migration strategy from the old website.

Where old product data can be exported:

* Import products
* Import categories
* Import descriptions
* Import prices
* Import images
* Import SKUs
* Import stock

Create scripts where appropriate.

Example:

```text
scripts/
    import_products.py
    import_categories.py
    migrate_old_urls.py
```

Do not destroy old data during migration.

---

# 75. TESTING

Create tests for:

## Products

* Product creation
* Product slug
* Product availability
* Product variants

## Cart

* Add product
* Remove product
* Quantity update
* Guest cart
* Authenticated cart
* Out-of-stock product

## Checkout

* Validation
* Order creation
* Total calculation
* Delivery calculation

## Payments

* Pending
* Success
* Failure
* Callback verification

## Orders

* Status changes
* Historical pricing
* Customer ownership

## Authentication

* Login
* Logout
* Registration
* Password reset

## Security

* CSRF
* Unauthorized access
* Admin permissions

---

# 76. TESTING COMMANDS

The final project must work with:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

No critical errors should remain.

---

# 77. CODE QUALITY

Write production-quality Django code.

Follow:

* PEP 8
* DRY principles
* Reusable templates
* Reusable components
* Class-based views where useful
* Function-based views where simpler
* Services for business logic
* Proper model constraints
* Proper validation

Do not put all business logic inside templates or views.

---

# 78. REUSABLE TEMPLATE COMPONENTS

Create components such as:

```text
components/
    header.html
    footer.html
    product_card.html
    product_badge.html
    rating.html
    cart_drawer.html
    breadcrumbs.html
    pagination.html
    toast.html
    modal.html
    mobile_nav.html
    newsletter.html
    trust_strip.html
```

Use template inheritance:

```text
base.html
```

---

# 79. JAVASCRIPT

Use modern vanilla JavaScript.

Create modules for:

```text
cart.js
wishlist.js
search.js
checkout.js
filters.js
product.js
navigation.js
```

Avoid a huge single JavaScript file.

Use fetch/AJAX where it improves UX.

Always provide graceful fallback behavior.

---

# 80. API-READY ARCHITECTURE

Even though the current project uses Django Templates, structure business logic so the system can later expose APIs.

Do not tightly couple everything to HTML rendering.

This will make future:

* mobile app
* partner integrations
* marketplace integrations
* WhatsApp automation

easier.

Do NOT install Django REST Framework unless there is an actual current requirement for API endpoints.

---

# 81. FUTURE EXPANSION

Architect the system so it can later support:

* Multiple branches
* Multiple delivery zones
* Wholesale customers
* Hospital/clinic accounts
* Bulk orders
* Corporate customers
* Product quotations
* Appointment/service booking
* Inventory management
* Supplier management
* Advanced analytics
* Mobile application

Do not implement unnecessary complexity now.

---

# 82. ADMIN BUSINESS CONTROLS

The owner must be able to manage the store without editing code.

Admin should make it possible to:

```text
Add product
Edit product
Delete product
Change price
Change stock
Upload images
Create category
Create discount
View order
Change order status
Confirm payment
Manage reviews
Publish article
Edit homepage
Edit contact details
Manage FAQs
Manage delivery fees
```

---

# 83. SEO-FRIENDLY PRODUCT CONTENT

Product pages should be designed to rank organically.

Include:

* Product name
* Product-specific description
* Features
* Specifications
* FAQs
* Related products
* Internal links

Avoid keyword stuffing.

---

# 84. RELATED PRODUCTS

Product pages should dynamically display:

```text
You may also like
```

and:

```text
Frequently bought together
```

based on category/product relationships.

Do not fabricate purchase data.

If real purchase data isn't available, use category-based recommendations.

---

# 85. RECENTLY VIEWED PRODUCTS

For anonymous users, use browser/session storage.

Display:

```text
Recently Viewed
```

where appropriate.

---

# 86. BREADCRUMBS

Example:

```text
Home
  >
Shop
  >
Orthopedic Supports
  >
Knee Support Brace
```

Use semantic markup.

Prepare breadcrumb schema.

---

# 87. SEARCH ENGINE FRIENDLINESS

Ensure:

* Clean URLs
* Canonical URLs
* No duplicate product URLs
* Correct pagination
* Metadata
* Sitemap
* Robots.txt
* Structured data
* Fast loading
* Mobile-first design

---

# 88. SECURITY FOR E-COMMERCE

Pay special attention to:

* Price manipulation
* Quantity manipulation
* Coupon manipulation
* Unauthorized order access
* Payment callback spoofing
* CSRF
* Session attacks
* File upload vulnerabilities
* Admin access
* IDOR vulnerabilities

Never trust:

```text
price
discount
total
payment status
customer ID
order ownership
```

sent from the browser.

Always calculate/verify these server-side.

---

# 89. PAYMENT SECURITY

Payment callbacks must:

1. Validate the request.
2. Verify transaction/reference.
3. Match amount.
4. Match order.
5. Match currency.
6. Prevent duplicate processing.
7. Record transaction.
8. Update order atomically.

Payment processing must be idempotent.

---

# 90. ORDER SECURITY

A customer must never be able to access another customer's order simply by changing:

```text
/order/123/
```

or:

```text
/order/124/
```

Use proper ownership checks.

---

# 91. PERFORMANCE TARGET

Aim for excellent Lighthouse performance.

Prioritize:

* LCP
* CLS
* INP
* TTFB

Avoid unnecessary JavaScript.

Avoid massive hero images.

Use lazy loading.

Optimize database queries.

---

# 92. RESPONSIVE PRODUCT GRID

Desktop:

```text
4 products per row
```

Tablet:

```text
3 products per row
```

Mobile:

```text
2 products per row
```

For very narrow devices, ensure product cards remain usable.

Product cards must not become excessively tiny.

---

# 93. MOBILE BOTTOM NAVIGATION

Consider a mobile bottom navigation:

```text
Home
Shop
Search
Wishlist
Cart
```

Keep it subtle and useful.

Cart should show item count.

---

# 94. MODERN GEN-Z UX DETAILS

The website should feel modern without becoming childish.

Use:

* Short copy
* Strong visual hierarchy
* Large product photography
* Quick actions
* Swipe-friendly components
* Sticky actions
* Modern cards
* Product badges
* Smooth micro-interactions
* Social proof
* Easy WhatsApp access

Avoid:

* excessive emojis
* slang
* childish language
* TikTok-style gimmicks

This is still a healthcare/medical commerce business.

---

# 95. TRUST-FIRST DESIGN

Because users are purchasing healthcare-related products, prominently communicate legitimate trust signals.

Possible:

```text
Quality Products
Secure Checkout
Kenya-wide Delivery
Responsive Customer Support
```

Only display certifications, professional affiliations, licenses, or guarantees if the owner provides verified information.

Never invent certifications.

---

# 96. HOMEPAGE CONVERSION FLOW

The homepage should naturally guide the user:

```text
DISCOVER
   ↓
CHOOSE CATEGORY
   ↓
EXPLORE PRODUCTS
   ↓
VIEW PRODUCT
   ↓
ADD TO CART
   ↓
CHECKOUT
   ↓
PAY
   ↓
ORDER CONFIRMED
```

Every major section should support this journey.

---

# 97. CTA HIERARCHY

Primary CTA:

```text
SHOP NOW
```

Secondary:

```text
EXPLORE PRODUCTS
```

Support CTA:

```text
CHAT ON WHATSAPP
```

Avoid having 10 competing CTAs in one viewport.

---

# 98. FOOTER

Create a premium footer.

Columns:

```text
ORTHOBEST CARE HUB

About
Shop
Services
Contact

SHOP
Categories
New Arrivals
Best Sellers
Offers

CUSTOMER CARE
Shipping
Returns
FAQs
Contact Us

INFORMATION
Privacy
Terms
Cookie Policy

CONNECT
WhatsApp
Facebook
Instagram
TikTok
```

Bottom:

```text
© 2026 Orthobest Care Hub. All rights reserved.
```

Use dynamic year.

---

# 99. ADMIN SETTINGS MODEL

Create a SiteSettings singleton containing:

* Site name
* Logo
* Favicon
* Email
* Phone
* WhatsApp
* Address
* Opening hours
* Social links
* Currency
* Announcement
* Footer text
* Default SEO title
* Default SEO description
* Google Analytics ID
* Meta Pixel ID

Do not hardcode these values.

---

# 100. FAVICON / BRAND ASSETS

Support:

* Logo
* Mobile logo
* Favicon
* OG image

All should be replaceable through admin or static assets.

---

# 101. DOCUMENTATION

Create a detailed README.

Include:

## Installation

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Database:

```bash
python manage.py migrate
```

Create admin:

```bash
python manage.py createsuperuser
```

Run:

```bash
python manage.py runserver
```

Also document:

* Environment variables
* PostgreSQL
* Static files
* Media files
* Production deployment
* Domain configuration
* HTTPS
* Payment configuration
* Email configuration
* M-Pesa callback configuration

---

# 102. PRODUCTION DEPLOYMENT READINESS

Prepare for deployment using:

* Gunicorn
* Nginx
* PostgreSQL
* HTTPS
* Static files
* Media files
* Environment variables

Do not include production secrets.

---

# 103. DOMAIN CONFIGURATION

Configure:

```text
orthobestcarehub.co.ke
www.orthobestcarehub.co.ke
```

Prepare:

```python
ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS
```

correctly.

Force HTTPS in production.

---

# 104. OLD DOMAIN REDIRECTION

Prepare:

```text
orthobestcarerehab.co.ke
www.orthobestcarerehab.co.ke
```

to redirect to:

```text
orthobestcarehub.co.ke
```

with permanent 301 redirects.

Create URL mapping for important old URLs.

---

# 105. NO PLACEHOLDER DESIGN

Do not deliver a website consisting of:

```text
Lorem ipsum
Product 1
Product 2
Service 1
Example Company
```

Use real existing business information wherever available.

If information cannot be obtained from the old website, create clearly identifiable admin-editable placeholder content.

---

# 106. NO FAKE PRODUCTS

Never invent:

* Product brands
* Medical claims
* Prices
* Stock
* Reviews
* Certifications
* Doctors
* Testimonials
* Locations

unless explicitly supplied by the business owner.

For reviews/testimonials, either migrate verified existing ones or leave the section empty until real content is added.

---

# 107. MIGRATION SAFETY

Before changing the database:

Create backups.

Never run destructive migrations against production without confirmation.

Never delete old product information automatically.

Create import scripts that can be tested.

---

# 108. FINAL QUALITY CHECK

Before declaring the project complete, verify:

### Frontend

* [ ] Homepage works
* [ ] Navigation works
* [ ] Mobile navigation works
* [ ] Search works
* [ ] Categories work
* [ ] Products work
* [ ] Product images work
* [ ] Product variants work
* [ ] Wishlist works
* [ ] Cart works
* [ ] Checkout works
* [ ] Order confirmation works
* [ ] Account works
* [ ] Contact form works
* [ ] Blog works
* [ ] FAQ works
* [ ] Footer works

### E-commerce

* [ ] Prices calculate correctly
* [ ] Quantities calculate correctly
* [ ] Discounts calculate correctly
* [ ] Delivery calculates correctly
* [ ] Stock is protected
* [ ] Orders are created correctly
* [ ] Payment status is reliable
* [ ] Payment callbacks are secure

### SEO

* [ ] Sitemap
* [ ] Robots.txt
* [ ] Canonicals
* [ ] Meta titles
* [ ] Meta descriptions
* [ ] Product schema
* [ ] Breadcrumb schema
* [ ] Open Graph
* [ ] 301 redirects

### Security

* [ ] CSRF
* [ ] Authentication
* [ ] Authorization
* [ ] Secure admin
* [ ] Secure payments
* [ ] No secrets committed
* [ ] File upload validation
* [ ] Customer order privacy

### Performance

* [ ] Optimized images
* [ ] Lazy loading
* [ ] Efficient queries
* [ ] Minimal JS
* [ ] Mobile performance
* [ ] No layout shifts

---

# 109. DEVELOPMENT WORKFLOW

Follow this exact development sequence.

## PHASE 1 — AUDIT

Inspect the existing website.

Document:

```text
Existing pages
Existing URLs
Existing categories
Existing products
Existing checkout
Existing payment flow
Existing content
Existing business information
Existing SEO
```

Create:

```text
OLD_SITE_AUDIT.md
```

---

## PHASE 2 — ARCHITECTURE

Design:

```text
Django apps
Models
URLs
Templates
Services
Database relationships
Payment architecture
```

Create:

```text
ARCHITECTURE.md
```

---

## PHASE 3 — DATABASE

Build:

* Categories
* Products
* Variants
* Images
* Customers
* Orders
* Payments
* Reviews
* Wishlist
* Blog
* FAQs
* Delivery
* Coupons
* Site settings

Create migrations.

---

## PHASE 4 — ADMIN

Build a professional Django admin experience.

Populate sample data only when necessary for development.

Clearly identify development/sample data.

---

## PHASE 5 — DESIGN SYSTEM

Build:

* Base template
* Header
* Footer
* Buttons
* Cards
* Forms
* Alerts
* Modals
* Product cards
* Navigation
* Responsive layout

---

## PHASE 6 — HOMEPAGE

Build the complete homepage.

---

## PHASE 7 — SHOP

Build:

* Shop
* Category
* Search
* Filters
* Sorting
* Product listing

---

## PHASE 8 — PRODUCT

Build:

* Product detail
* Gallery
* Variants
* Wishlist
* Add to cart
* Related products
* Reviews

---

## PHASE 9 — CART

Build:

* Session cart
* Cart drawer
* Cart page
* Quantity management
* Price calculation

---

## PHASE 10 — CHECKOUT

Build:

* Customer details
* Delivery
* Order summary
* Payment selection
* Validation

---

## PHASE 11 — PAYMENTS

Implement the approved payment provider.

Keep provider credentials in `.env`.

Implement callbacks securely.

---

## PHASE 12 — ORDERS

Build:

* Order creation
* Order tracking
* Customer account
* Admin order management
* Email notifications

---

## PHASE 13 — CONTENT

Build:

* About
* Services
* Blog
* FAQ
* Contact
* Policies

---

## PHASE 14 — SEO

Implement:

* Sitemap
* Robots
* Schema
* Metadata
* Canonicals
* Redirects

---

## PHASE 15 — PERFORMANCE & SECURITY

Run:

```bash
python manage.py check --deploy
```

Fix every important warning.

---

## PHASE 16 — TESTING

Run all automated tests.

Manually test:

```text
Homepage
Search
Product
Cart
Checkout
Payment
Order
Account
Admin
Mobile
```

---

# 110. IMPORTANT CODING AGENT BEHAVIOR

Do not stop after creating models.

Do not stop after creating templates.

Do not generate only a UI mockup.

Build the actual working application.

Do not fake cart functionality.

Do not fake checkout functionality.

Do not fake payment success.

Do not hardcode product prices.

Do not hardcode order totals.

Do not hardcode customer data.

Do not expose admin functionality publicly.

Do not skip validation.

Do not use placeholder buttons that do nothing.

Every visible interactive element should either work or be intentionally disabled until its backend functionality exists.

---

# 111. WHEN INFORMATION IS MISSING

If you cannot access a particular part of the old website:

DO NOT invent it.

Instead:

1. Record it in `OLD_SITE_AUDIT.md`.
2. Create the appropriate Django model/field.
3. Make the content admin-editable.
4. Continue development.
5. Clearly report what needs owner confirmation.

Example:

```text
MISSING INFORMATION:
Old website payment provider could not be verified.

IMPLEMENTATION:
PaymentGateway abstraction created.

OWNER ACTION:
Confirm the actual payment provider and credentials before production.
```

---

# 112. FINAL DELIVERABLE

The finished repository should contain:

```text
Working Django application
PostgreSQL support
Modern responsive frontend
Complete e-commerce functionality
Product management
Category management
Cart
Wishlist
Checkout
Payment architecture
Orders
Customer accounts
Reviews
Blog
FAQ
Contact
Newsletter
SEO
Sitemap
Robots.txt
301 migration support
Django Admin
Tests
Documentation
Environment configuration
Deployment instructions
```

---

# 113. FINAL UI STANDARD

The finished website should look like it was designed by a professional 2026 digital product/e-commerce team.

The visitor should immediately feel:

> "This is a legitimate, modern healthcare product store."

The website should combine:

**Healthcare Trust + Modern E-commerce + Kenyan Convenience + Gen-Z UX**

without sacrificing professionalism.

The design must be:

* Premium
* Clean
* Fast
* Accessible
* Mobile-first
* Conversion-focused
* Trustworthy
* Modern
* Easy to manage
* SEO-friendly
* Production-ready

---

# 114. MOST IMPORTANT INSTRUCTION

DO NOT blindly copy the visual design of the existing website.

The existing website is the **business/content/functionality reference**.

The new website should be a **complete modernization**.

Preserve the business's useful:

* Products
* Services
* Categories
* Contact information
* Policies
* Existing SEO-relevant URLs
* Business information

but redesign the experience from the ground up.

The final result should feel like:

# ORTHOBEST CARE HUB

### A modern Kenyan destination for orthopedic, rehabilitation, mobility and healthcare-support products.

Build the project systematically.

Do not skip phases.

Do not claim a feature is complete until it actually works.

At the end of every major phase, run the relevant Django checks/tests and fix errors before continuing.

When finished, provide:

1. Complete project structure
2. Database/model summary
3. URL map
4. Admin capabilities
5. Payment architecture
6. SEO/migration strategy
7. Testing results
8. Remaining owner-provided information required
9. Local development instructions
10. Production deployment instructions
