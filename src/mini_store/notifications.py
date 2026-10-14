
"""Customer notification behavior."""

class NotificationService:
    def __init__(self, email_sender, sms_sender, push_sender):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.push_sender = push_sender

    # Shared notification dispatcher
    def _send_notification(self, customer, payload_builders) -> None:
        """Route a notification through the preferred channel.

        ``payload_builders`` maps channel names to zero-argument callables.
        Email and push builders return (subject_or_title, message), while
        SMS builders return (message,). Only the selected builder is called.
        Unknown channels raise ValueError without sending a notification.
        """
        channel = customer.preferred_channel

        if channel == "email":
            subject, message = payload_builders["email"]()
            self.email_sender.send(customer.email, subject, message)

        elif channel == "sms":
            (message,) = payload_builders["sms"]()
            self.sms_sender.send(customer.phone, message)

        elif channel == "push":
            title, message = payload_builders["push"]()
            self.push_sender.send(customer.device_id, title, message)

        else:
            raise ValueError("Unsupported notification channel")

    # Order confirmation uses the shared dispatcher
    def send_order_confirmation(self, customer, order_id: str) -> None:
        self._send_notification(
            customer,
            {
                "email": lambda: (
                    f"Order {order_id} confirmed",
                    f"Hello {customer.name}, your order {order_id} was confirmed.",
                ),
                "sms": lambda: (
                    f"Order {order_id} confirmed for {customer.name}.",
                ),
                "push": lambda: (
                    "Order confirmed",
                    f"Order {order_id} is confirmed.",
                ),
            },
        )

    # Shipping update uses the same dispatcher
    def send_shipping_update(
        self, customer, order_id: str, tracking_code: str
    ) -> None:
        self._send_notification(
            customer,
            {
                "email": lambda: (
                    f"Order {order_id} shipped",
                    (
                        f"Hello {customer.name}, your order {order_id} shipped. "
                        f"Tracking: {tracking_code}."
                    ),
                ),
                "sms": lambda: (
                    f"Order {order_id} shipped. Tracking: {tracking_code}.",
                ),
                "push": lambda: (
                    "Order shipped",
                    f"Track order {order_id}: {tracking_code}.",
                ),
            },
        )
