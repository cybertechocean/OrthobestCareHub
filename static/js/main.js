/**
 * ORTHOBEST CARE HUB — JAVASCRIPT APP MODULE (2026)
 * Handles Cart Drawer, Live Autocomplete Search, AJAX Checkout, M-Pesa Polling & Toasts.
 */

document.addEventListener('DOMContentLoaded', () => {
  initCSRF();
  initCartDrawer();
  initLiveSearch();
  initProductTabs();
  initProductGallery();
  initCheckoutInteractions();
  initMpesaPayment();
  initNewsletterForm();
  initWishlist();
  initCookieConsent();
});

// 1. Helper to extract Django CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let csrfToken = null;
function initCSRF() {
  csrfToken = getCookie('csrftoken');
}

// 2. Toast Notification System
window.showToast = function(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <div style="font-size: 1.2rem;">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</div>
    <div style="flex-grow: 1; font-size: 0.875rem; font-weight: 500;">${message}</div>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
};

// 3. Mini-Cart Drawer & AJAX Cart Operations
function initCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  const openBtns = document.querySelectorAll('[data-toggle-cart]');
  const closeBtn = document.getElementById('closeCartDrawer');

  function openDrawer() {
    if (drawer && overlay) {
      drawer.classList.add('active');
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    if (drawer && overlay) {
      drawer.classList.remove('active');
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  openBtns.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openDrawer();
  }));

  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);

  // Global AJAX Add-To-Cart handler
  document.addEventListener('submit', function(e) {
    const form = e.target.closest('.ajax-cart-form');
    if (!form) return;

    e.preventDefault();
    const actionUrl = form.getAttribute('action');
    const formData = new FormData(form);
    formData.append('ajax', '1');

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Adding...</span>';
    }

    fetch(actionUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
      if (data.success) {
        // Update badge counts across page
        document.querySelectorAll('.badge-count').forEach(el => {
          el.textContent = data.cart_total_count;
        });

        // Update drawer subtotals
        const drawerSubtotal = document.getElementById('drawerSubtotal');
        if (drawerSubtotal) drawerSubtotal.textContent = data.cart_subtotal;

        showToast(data.message, 'success');
        openDrawer();
        
        // Reload drawer content
        reloadDrawerCart();
      } else {
        showToast(data.message || 'Error adding item', 'error');
      }
    })
    .catch(err => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
      showToast('Could not add to cart. Please refresh and try again.', 'error');
    });
  });
}

function reloadDrawerCart() {
  const drawerBody = document.querySelector('.drawer-body');
  if (!drawerBody) return;
  // If drawer template includes live list or full reload
  fetch('/cart/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(r => r.text())
    .then(() => {
      // Re-fetch badge count
    });
}

// 4. Live Search Autocomplete
function initLiveSearch() {
  const inputs = document.querySelectorAll('.search-input');
  
  inputs.forEach(input => {
    let timeout = null;
    const parent = input.closest('.search-widget') || input.parentElement;
    let suggestionsBox = parent.querySelector('.search-suggestions');

    if (!suggestionsBox) {
      suggestionsBox = document.createElement('div');
      suggestionsBox.className = 'search-suggestions';
      parent.appendChild(suggestionsBox);
    }

    input.addEventListener('input', () => {
      clearTimeout(timeout);
      const query = input.value.trim();
      if (query.length < 2) {
        suggestionsBox.classList.remove('active');
        suggestionsBox.innerHTML = '';
        return;
      }

      timeout = setTimeout(() => {
        fetch(`/api/products/search/?q=${encodeURIComponent(query)}`)
          .then(res => res.json())
          .then(data => {
            if (data.results && data.results.length > 0) {
              suggestionsBox.innerHTML = data.results.map(item => `
                <a href="${item.url}" class="suggestion-item">
                  <img src="${item.image}" alt="${item.name}" class="suggestion-thumb" />
                  <div style="flex-grow: 1;">
                    <div style="font-weight: 700; font-size: 0.875rem; color: var(--secondary);">${item.name}</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">${item.category} • SKU: ${item.sku}</div>
                    <div style="font-size: 0.875rem; font-weight: 800; color: var(--primary);">${item.price}</div>
                  </div>
                </a>
              `).join('');
              suggestionsBox.classList.add('active');
            } else {
              suggestionsBox.innerHTML = `<div style="padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">No products found for "${query}"</div>`;
              suggestionsBox.classList.add('active');
            }
          });
      }, 250);
    });

    document.addEventListener('click', (e) => {
      if (!parent.contains(e.target)) {
        suggestionsBox.classList.remove('active');
      }
    });
  });
}

// 5. Product Tabs Switching
function initProductTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      const container = btn.closest('.product-tabs-container') || document;

      container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// 6. Product Detail Gallery Switching
function initProductGallery() {
  const mainImg = document.getElementById('mainProductImage');
  const thumbs = document.querySelectorAll('.thumb-item');

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
      const newSrc = thumb.getAttribute('data-full-src');
      if (mainImg && newSrc) {
        mainImg.src = newSrc;
      }
    });
  });
}

// 7. Checkout Dynamic Calculations & Coupon Validation
function initCheckoutInteractions() {
  const deliverySelect = document.getElementById('delivery_zone_select');
  const deliveryDisplay = document.getElementById('summaryDeliveryFee');
  const totalDisplay = document.getElementById('summaryTotal');
  const applyCouponBtn = document.getElementById('applyCouponBtn');
  const couponInput = document.getElementById('coupon_code_input');

  if (deliverySelect) {
    deliverySelect.addEventListener('change', updateCheckoutSummary);
  }

  if (applyCouponBtn && couponInput) {
    applyCouponBtn.addEventListener('click', () => {
      const code = couponInput.value.trim();
      if (!code) {
        showToast('Please enter a coupon code.', 'warning');
        return;
      }

      const subtotalVal = parseFloat(document.getElementById('checkoutSubtotalVal').value || 0);

      const formData = new FormData();
      formData.append('code', code);
      formData.append('subtotal', subtotalVal);

      fetch('/api/coupon/validate/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrfToken }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          showToast(data.message, 'success');
          const discountDisplay = document.getElementById('summaryDiscount');
          if (discountDisplay) discountDisplay.textContent = `- ${data.discount_formatted}`;
          document.getElementById('checkoutDiscountVal').value = data.discount_amount;
          updateCheckoutSummary();
        } else {
          showToast(data.message, 'error');
        }
      });
    });
  }

  function updateCheckoutSummary() {
    const subtotal = parseFloat(document.getElementById('checkoutSubtotalVal')?.value || 0);
    const discount = parseFloat(document.getElementById('checkoutDiscountVal')?.value || 0);
    
    let deliveryFee = 0;
    if (deliverySelect && deliverySelect.selectedOptions[0]) {
      const feeAttr = deliverySelect.selectedOptions[0].getAttribute('data-fee');
      deliveryFee = parseFloat(feeAttr || 0);
    }

    const finalTotal = Math.max(0, subtotal + deliveryFee - discount);

    if (deliveryDisplay) deliveryDisplay.textContent = `KSh ${deliveryFee.toLocaleString()}`;
    if (totalDisplay) totalDisplay.textContent = `KSh ${finalTotal.toLocaleString()}`;
  }
}

// 8. Safaricom M-Pesa STK Push Polling & Trigger
function initMpesaPayment() {
  const triggerBtn = document.getElementById('initiateMpesaStkBtn');
  if (!triggerBtn) return;

  triggerBtn.addEventListener('click', () => {
    const orderNumber = triggerBtn.getAttribute('data-order');
    const phoneInput = document.getElementById('mpesaPhoneInput');
    const phone = phoneInput ? phoneInput.value : '';

    triggerBtn.disabled = true;
    triggerBtn.innerHTML = '<span>Sending STK Prompt to Phone...</span>';

    const formData = new FormData();
    formData.append('phone', phone);

    fetch(`/payments/mpesa/stk-push/${orderNumber}/`, {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrfToken }
    })
    .then(r => r.json())
    .then(data => {
      triggerBtn.disabled = false;
      triggerBtn.innerHTML = '<span>Resend M-Pesa STK Prompt</span>';

      const promptBox = document.getElementById('mpesaPromptNotice');
      if (promptBox) {
        promptBox.style.display = 'block';
        promptBox.innerHTML = `<strong>${data.message}</strong>`;
      }

      if (data.is_simulation) {
        const simBox = document.getElementById('simulationBox');
        if (simBox) {
          simBox.style.display = 'block';
          simBox.setAttribute('data-checkout-id', data.checkout_request_id);
        }
      }

      // Start status check polling every 3 seconds
      pollPaymentStatus(orderNumber);
    });
  });

  // Simulated confirmation button for developer/testing
  const simConfirmBtn = document.getElementById('simConfirmBtn');
  if (simConfirmBtn) {
    simConfirmBtn.addEventListener('click', () => {
      const simBox = document.getElementById('simulationBox');
      const checkoutId = simBox.getAttribute('data-checkout-id');

      fetch(`/payments/mpesa/simulate-confirm/${checkoutId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }
      })
      .then(r => r.json())
      .then(res => {
        if (res.success) {
          showToast(res.message, 'success');
          setTimeout(() => {
            window.location.href = `/order/confirmed/${triggerBtn.getAttribute('data-order')}/`;
          }, 1000);
        }
      });
    });
  }
}

function pollPaymentStatus(orderNumber) {
  let attempts = 0;
  const maxAttempts = 30; // 90 seconds
  const interval = setInterval(() => {
    attempts++;
    if (attempts > maxAttempts) {
      clearInterval(interval);
      return;
    }

    fetch(`/payments/mpesa/status-check/${orderNumber}/`)
      .then(r => r.json())
      .then(data => {
        if (data.is_paid) {
          clearInterval(interval);
          showToast('M-Pesa payment received successfully! Redirecting...', 'success');
          setTimeout(() => {
            window.location.href = `/order/confirmed/${orderNumber}/`;
          }, 1200);
        }
      });
  }, 3000);
}

// 9. Newsletter AJAX Form
function initNewsletterForm() {
  const form = document.querySelector('.newsletter-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = form.querySelector('.newsletter-input');
    const email = input.value.trim();

    const formData = new FormData();
    formData.append('email', email);

    fetch('/api/newsletter/subscribe/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrfToken }
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        showToast(data.message, 'success');
        input.value = '';
      } else {
        showToast(data.message, 'error');
      }
    });
  });
}

// 10. Wishlist AJAX Toggle Handler
function initWishlist() {
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('.wishlist-toggle-btn');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    const productId = btn.getAttribute('data-product-id');
    if (!productId) return;

    fetch(`/wishlist/toggle/${productId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        // Toggle active class on all buttons corresponding to this product
        const allMatchingBtns = document.querySelectorAll(`.wishlist-toggle-btn[data-product-id="${productId}"]`);
        allMatchingBtns.forEach(b => {
          const svg = b.querySelector('svg');
          if (data.in_wishlist) {
            b.classList.add('active');
            b.setAttribute('title', 'Remove from Wishlist');
            if (svg) svg.setAttribute('fill', '#FBD420');
          } else {
            b.classList.remove('active');
            b.setAttribute('title', 'Save to Wishlist');
            if (svg) svg.setAttribute('fill', 'none');
          }
        });

        // Update all wishlist badge counters
        const badges = document.querySelectorAll('.wishlist-badge-count');
        badges.forEach(badge => {
          badge.textContent = data.total_count;
        });

        showToast(data.message, data.in_wishlist ? 'success' : 'info');
      } else {
        showToast(data.message || 'Could not update wishlist.', 'error');
      }
    })
    .catch(err => {
      showToast('Network error while updating wishlist.', 'error');
    });
  });
}

// 11. Cookie Consent & Preferences Management
function initCookieConsent() {
  const banner = document.getElementById('cookieBanner');
  const modal = document.getElementById('cookieModalOverlay');
  const acceptBtn = document.getElementById('cookieAcceptBtn');
  const rejectBtn = document.getElementById('cookieRejectBtn');
  const settingsBtn = document.getElementById('cookieSettingsBtn');
  const closeModalBtn = document.getElementById('closeCookieModal');
  const savePrefsBtn = document.getElementById('saveCookiePrefsBtn');

  const STORAGE_KEY = 'orthobest_cookie_consent';
  const savedConsent = localStorage.getItem(STORAGE_KEY);

  // If consent not stored, reveal banner
  if (!savedConsent && banner) {
    setTimeout(() => {
      banner.style.display = 'block';
    }, 600);
  }

  function saveConsent(essential, functional, analytics) {
    const prefs = {
      essential: true,
      functional: !!functional,
      analytics: !!analytics,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    if (banner) banner.style.display = 'none';
    if (modal) modal.style.display = 'none';
    showToast('Cookie preferences saved successfully.', 'success');
  }

  if (acceptBtn) {
    acceptBtn.addEventListener('click', () => {
      saveConsent(true, true, true);
    });
  }

  if (rejectBtn) {
    rejectBtn.addEventListener('click', () => {
      saveConsent(true, false, false);
    });
  }

  if (settingsBtn) {
    settingsBtn.addEventListener('click', () => {
      if (modal) modal.style.display = 'flex';
    });
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      if (modal) modal.style.display = 'none';
    });
  }

  if (savePrefsBtn) {
    savePrefsBtn.addEventListener('click', () => {
      const func = document.getElementById('prefFunctional')?.checked ?? true;
      const anal = document.getElementById('prefAnalytics')?.checked ?? true;
      saveConsent(true, func, anal);
    });
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
      }
    });
  }
}

