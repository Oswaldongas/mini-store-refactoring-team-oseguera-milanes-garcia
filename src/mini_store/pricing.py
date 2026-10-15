"""Pricing rules for orders."""

# --- Business Rule Constants ---
DISCOUNT_RATE_PREMIUM = 0.10
DISCOUNT_RATE_EMPLOYEE = 0.15

COUPON_SAVE5_RATE = 0.05
COUPON_SAVE20_RATE = 0.20
COUPON_SAVE20_MIN_SUBTOTAL = 1500

TAX_RATE_MX = 0.16

SHIPPING_MX_THRESHOLD = 1000
SHIPPING_MX_FREE = 0.0
SHIPPING_MX_STANDARD = 99.0

SHIPPING_INTL_THRESHOLD = 2000
SHIPPING_INTL_REDUCED = 199.0
SHIPPING_INTL_STANDARD = 299.0

def _calculate_discount(subtotal: float, customer_type: str, coupon_code: str | None) -> float:
    """Calculate the total discount amount based on customer type and coupons."""
    discount = 0.0

    if customer_type == "premium":
        discount = subtotal * DISCOUNT_RATE_PREMIUM
    elif customer_type == "employee":
        discount = subtotal * DISCOUNT_RATE_EMPLOYEE

    if coupon_code == "SAVE5":
        discount += subtotal * COUPON_SAVE5_RATE
    elif coupon_code == "SAVE20" and subtotal >= COUPON_SAVE20_MIN_SUBTOTAL:
        discount += subtotal * COUPON_SAVE20_RATE

    return discount

def _calculate_tax(discounted_subtotal: float, country: str) -> float:
    """Calculate the tax amount based on the country."""
    if country == "MX":
        return discounted_subtotal * TAX_RATE_MX
    return 0.0

def _calculate_shipping(discounted_subtotal: float, country: str) -> float:
    """Calculate shipping costs based on subtotal thresholds and country."""
    if country == "MX":
        if discounted_subtotal >= SHIPPING_MX_THRESHOLD:
            return SHIPPING_MX_FREE
        return SHIPPING_MX_STANDARD
    else:
        if discounted_subtotal >= SHIPPING_INTL_THRESHOLD:
            return SHIPPING_INTL_REDUCED
        return SHIPPING_INTL_STANDARD

def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Return the final order total after discounts, tax, and shipping."""
    discount = _calculate_discount(subtotal, customer_type, coupon_code)
    
    # Refactorización: uso de max() para evitar que el subtotal sea negativo
    discounted_subtotal = max(0.0, subtotal - discount)
        
    tax = _calculate_tax(discounted_subtotal, country)
    shipping = _calculate_shipping(discounted_subtotal, country)

    return round(discounted_subtotal + tax + shipping, 2)