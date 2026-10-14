"""Pricing rules for orders."""

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

def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Return the final order total after discounts, tax, and shipping."""
    discount = 0.0

    if customer_type == "premium":
        discount = subtotal * DISCOUNT_RATE_PREMIUM
    elif customer_type == "employee":
        discount = subtotal * DISCOUNT_RATE_EMPLOYEE

    if coupon_code == "SAVE5":
        discount += subtotal * COUPON_SAVE5_RATE
    elif coupon_code == "SAVE20" and subtotal >= COUPON_SAVE20_MIN_SUBTOTAL:
        discount += subtotal * COUPON_SAVE20_RATE

    discounted_subtotal = subtotal - discount

    if discounted_subtotal < 0:
        discounted_subtotal = 0

    if country == "MX":
        tax = discounted_subtotal * TAX_RATE_MX
    else:
        tax = 0.0

    if country == "MX":
        if discounted_subtotal >= SHIPPING_MX_THRESHOLD:
            shipping = SHIPPING_MX_FREE
        else:
            shipping = SHIPPING_MX_STANDARD
    else:
        if discounted_subtotal >= SHIPPING_INTL_THRESHOLD:
            shipping = SHIPPING_INTL_REDUCED
        else:
            shipping = SHIPPING_INTL_STANDARD

    return round(discounted_subtotal + tax + shipping, 2)