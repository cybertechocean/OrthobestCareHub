import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.db.models import Q, Avg
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Product, Category, Brand, ProductReview
from .forms import ProductReviewForm
from .wishlist import WishlistService
from apps.cart.cart import Cart


class ShopView(ListView):
    model = Product
    template_name = "products/shop.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_available=True).select_related('category', 'brand').prefetch_related('images')
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Brand filter
        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)

        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Availability filter
        in_stock = self.request.GET.get('in_stock')
        if in_stock == '1':
            qs = qs.filter(stock_quantity__gt=0)

        # Search query
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query) |
                Q(short_description__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(brand__name__icontains=query)
            ).distinct()

        # Sorting
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'price-asc':
            qs = qs.order_by('price')
        elif sort == 'price-desc':
            qs = qs.order_by('-price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'bestseller':
            qs = qs.order_by('-is_bestseller', '-created_at')
        elif sort == 'name-asc':
            qs = qs.order_by('name')
        elif sort == 'name-desc':
            qs = qs.order_by('-name')
        else:  # 'featured'
            qs = qs.order_by('-is_featured', '-is_bestseller', '-created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).prefetch_related('products')
        context['brands'] = Brand.objects.filter(is_active=True)
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['selected_sort'] = self.request.GET.get('sort', 'featured')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['in_stock'] = self.request.GET.get('in_stock', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['total_count'] = self.get_queryset().count()
        return context


class CategoryDetailView(ShopView):
    template_name = "products/category_detail.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        qs = Product.objects.filter(category=self.category, is_available=True).select_related('category', 'brand').prefetch_related('images')
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Sorting
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'price-asc':
            qs = qs.order_by('price')
        elif sort == 'price-desc':
            qs = qs.order_by('-price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'bestseller':
            qs = qs.order_by('-is_bestseller', '-created_at')
        else:
            qs = qs.order_by('-is_featured', '-is_bestseller', '-created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_available=True).select_related('category', 'brand').prefetch_related('images', 'variants', 'reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['review_form'] = ProductReviewForm()
        context['approved_reviews'] = product.reviews.filter(approved=True)
        context['related_products'] = Product.objects.filter(
            category=product.category, 
            is_available=True
        ).exclude(id=product.id).select_related('category', 'brand').prefetch_related('images')[:4]
        
        # WhatsApp Pre-filled message
        site_phone = "254798246811"
        wa_text = f"Hello Orthobest Care Hub, I would like to inquire about '{product.name}' (SKU: {product.sku}, KSh {product.price:,.0f}). Please assist me."
        context['whatsapp_inquiry_url'] = f"https://wa.me/{site_phone}?text={urllib.parse.quote(wa_text)}"
        
        # Browsing History: Record product in session
        recently_viewed = self.request.session.get('recently_viewed', [])
        if product.id in recently_viewed:
            recently_viewed.remove(product.id)
        recently_viewed.insert(0, product.id)
        self.request.session['recently_viewed'] = recently_viewed[:12]
        self.request.session.modified = True

        # Fetch recently viewed products (excluding current product)
        recent_ids = [pid for pid in recently_viewed if pid != product.id][:4]
        if recent_ids:
            recent_products_dict = {p.id: p for p in Product.objects.filter(id__in=recent_ids, is_available=True).select_related('category').prefetch_related('images')}
            context['recently_viewed_products'] = [recent_products_dict[pid] for pid in recent_ids if pid in recent_products_dict]
        else:
            context['recently_viewed_products'] = []

        return context


class ProductReviewCreateView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_available=True)
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            messages.success(request, "Thank you! Your review has been submitted successfully.")
        else:
            messages.error(request, "Please check your review submission for errors.")
        return redirect('products:product_detail', slug=product.slug)


class ProductLiveSearchApiView(View):
    """Provides fast JSON autocomplete results for the search bar"""
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return JsonResponse({'results': []})

        products = Product.objects.filter(
            is_available=True
        ).filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category')[:8]

        results = []
        for p in products:
            img_url = p.primary_image.image.url if (p.primary_image and p.primary_image.image) else '/static/images/placeholder.svg'
            results.append({
                'name': p.name,
                'sku': p.sku,
                'price': f"KSh {p.price:,.0f}",
                'category': p.category.name,
                'url': p.get_absolute_url(),
                'image': img_url,
                'in_stock': p.in_stock,
            })

        return JsonResponse({'results': results})


class WishlistDetailView(View):
    """Renders the full Wishlist page"""
    def get(self, request):
        wishlist_service = WishlistService(request)
        products = wishlist_service.get_products()
        return render(request, "products/wishlist.html", {
            'products': products,
            'wishlist_count': wishlist_service.count(),
        })


class WishlistToggleAjaxView(View):
    """AJAX endpoint to add or remove an item from the Wishlist"""
    def post(self, request, product_id):
        try:
            wishlist_service = WishlistService(request)
            in_wishlist, total_count, product = wishlist_service.toggle(product_id)
            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist,
                'total_count': total_count,
                'product_name': product.name,
                'message': f"'{product.name}' {'added to' if in_wishlist else 'removed from'} your wishlist.",
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class WishlistRemoveView(View):
    """Removes a single item from the Wishlist and redirects back"""
    def post(self, request, product_id):
        wishlist_service = WishlistService(request)
        wishlist_service.remove(product_id)
        messages.success(request, "Product removed from your wishlist.")
        return redirect('products:wishlist')


class WishlistMoveToCartView(View):
    """Moves a product from the Wishlist to the Shopping Cart"""
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_available=True)
        cart = Cart(request)
        cart.add(product=product, quantity=1)
        
        wishlist_service = WishlistService(request)
        wishlist_service.remove(product_id)
        
        messages.success(request, f"'{product.name}' moved to your shopping cart!")
        return redirect('cart:cart_detail')


class ClearBrowsingHistoryView(View):
    """Clears the recently viewed browsing history from the session"""
    def post(self, request):
        if 'recently_viewed' in request.session:
            del request.session['recently_viewed']
            request.session.modified = True
        messages.success(request, "Your browsing history has been cleared.")
        next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/shop/'))
        return redirect(next_url)
