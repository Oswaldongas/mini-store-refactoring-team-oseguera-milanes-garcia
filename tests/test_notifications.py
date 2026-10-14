
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from mini_store.notifications import NotificationService


def make_customer(channel: str):
    return SimpleNamespace(
        name="Ana",
        preferred_channel=channel,
        email="ana@example.com",
        phone="+521234567890",
        device_id="device-1",
    )


def make_service():
    email = Mock()
    sms = Mock()
    push = Mock()

    service = NotificationService(email, sms, push)

    return service, email, sms, push


# TEST 1: Order confirmation via Email
def test_email_order_confirmation_is_sent():
    service, email, sms, push = make_service()

    service.send_order_confirmation(
        make_customer("email"), "A-100"
    )

    email.send.assert_called_once_with(
        "ana@example.com",
        "Order A-100 confirmed",
        "Hello Ana, your order A-100 was confirmed.",
    )

    sms.send.assert_not_called()
    push.send.assert_not_called()


# TEST 2: Order confirmation via SMS
def test_sms_order_confirmation_is_sent():
    service, email, sms, push = make_service()

    service.send_order_confirmation(
        make_customer("sms"), "A-100"
    )

    sms.send.assert_called_once_with(
        "+521234567890",
        "Order A-100 confirmed for Ana.",
    )

    email.send.assert_not_called()
    push.send.assert_not_called()


# TEST 3: Order confirmation via Push
def test_push_order_confirmation_is_sent():
    service, email, sms, push = make_service()

    service.send_order_confirmation(
        make_customer("push"), "A-100"
    )

    push.send.assert_called_once_with(
        "device-1",
        "Order confirmed",
        "Order A-100 is confirmed.",
    )

    email.send.assert_not_called()
    sms.send.assert_not_called()


# TEST 4: Shipping update via Email
def test_email_shipping_update_is_sent():
    service, email, sms, push = make_service()

    service.send_shipping_update(
        make_customer("email"),
        "A-100",
        "TRACK-9",
    )

    email.send.assert_called_once_with(
        "ana@example.com",
        "Order A-100 shipped",
        "Hello Ana, your order A-100 shipped. Tracking: TRACK-9.",
    )

    sms.send.assert_not_called()
    push.send.assert_not_called()


# TEST 5: Shipping update via SMS
def test_sms_shipping_update_is_sent():
    service, email, sms, push = make_service()

    service.send_shipping_update(
        make_customer("sms"),
        "A-100",
        "TRACK-9",
    )

    sms.send.assert_called_once_with(
        "+521234567890",
        "Order A-100 shipped. Tracking: TRACK-9.",
    )

    email.send.assert_not_called()
    push.send.assert_not_called()


# TEST 6: Shipping update via Push
def test_push_shipping_update_is_sent():
    service, email, sms, push = make_service()

    service.send_shipping_update(
        make_customer("push"),
        "A-100",
        "TRACK-9",
    )

    push.send.assert_called_once_with(
        "device-1",
        "Order shipped",
        "Track order A-100: TRACK-9.",
    )

    email.send.assert_not_called()
    sms.send.assert_not_called()


# TEST 7: Invalid channel for confirmation
def test_order_confirmation_rejects_unsupported_channel():
    service, email, sms, push = make_service()

    with pytest.raises(
        ValueError,
        match="^Unsupported notification channel$"
    ):
        service.send_order_confirmation(
            make_customer("whatsapp"), "A-100"
        )

    email.send.assert_not_called()
    sms.send.assert_not_called()
    push.send.assert_not_called()


# TEST 8: Invalid channel for shipping
def test_shipping_update_rejects_unsupported_channel():
    service, email, sms, push = make_service()

    with pytest.raises(
        ValueError,
        match="^Unsupported notification channel$"
    ):
        service.send_shipping_update(
            make_customer("whatsapp"),
            "A-100",
            "TRACK-9",
        )

    email.send.assert_not_called()
    sms.send.assert_not_called()
    push.send.assert_not_called()

