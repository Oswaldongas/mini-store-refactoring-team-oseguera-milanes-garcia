from mini_store.pricing import calculate_order_total


def test_standard_customer_in_mexico_pays_tax_and_shipping():
    assert calculate_order_total(500, "standard", None, "MX") == 679.0


def test_premium_customer_receives_discount():
    assert calculate_order_total(1000, "premium", None, "MX") == 1143.0


def test_save20_coupon_requires_minimum_subtotal():
    assert calculate_order_total(1400, "standard", "SAVE20", "MX") == 1624.0

def test_save5_coupon_applies_discount():
    assert calculate_order_total(1000, "standard", "SAVE5", "MX") == 1201.0

def test_save20_coupon_applies_when_subtotal_is_sufficient():
    assert calculate_order_total(2000, "standard", "SAVE20", "MX") == 1856.0

def test_negative_subtotal_is_corrected_to_zero():
    assert calculate_order_total(-100, "standard", None, "MX") == 99.0

def test_international_order_no_tax_and_high_shipping():
    assert calculate_order_total(1000, "standard", None, "US") == 1299.0
   