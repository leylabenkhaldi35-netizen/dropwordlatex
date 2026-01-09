import base64
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from subscriptions.models import Subscription
from users.models import User

from .models import Payment


class PayPalWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not verify_paypal_signature(request):
            return Response({"detail": "Invalid signature"}, status=400)

        event = request.data
        event_type = event.get("event_type")
        resource = event.get("resource", {})
        if event_type in {"BILLING.SUBSCRIPTION.ACTIVATED", "BILLING.SUBSCRIPTION.UPDATED"}:
            handle_subscription_update(resource, active=True)
        elif event_type in {"BILLING.SUBSCRIPTION.CANCELLED", "BILLING.SUBSCRIPTION.SUSPENDED"}:
            handle_subscription_update(resource, active=False)

        return Response({"status": "ok"})


def verify_paypal_signature(request) -> bool:
    auth = f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}".encode()
    basic_auth = base64.b64encode(auth).decode()
    access_token_resp = requests.post(
        f"{settings.PAYPAL_API_BASE}/v1/oauth2/token",
        headers={"Authorization": f"Basic {basic_auth}"},
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    access_token_resp.raise_for_status()
    access_token = access_token_resp.json()["access_token"]

    verification_payload = {
        "auth_algo": request.headers.get("PAYPAL-AUTH-ALGO"),
        "cert_url": request.headers.get("PAYPAL-CERT-URL"),
        "transmission_id": request.headers.get("PAYPAL-TRANSMISSION-ID"),
        "transmission_sig": request.headers.get("PAYPAL-TRANSMISSION-SIG"),
        "transmission_time": request.headers.get("PAYPAL-TRANSMISSION-TIME"),
        "webhook_id": settings.PAYPAL_WEBHOOK_ID,
        "webhook_event": request.data,
    }

    response = requests.post(
        f"{settings.PAYPAL_API_BASE}/v1/notifications/verify-webhook-signature",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        json=verification_payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("verification_status") == "SUCCESS"


def handle_subscription_update(resource: dict, active: bool) -> None:
    subscriber = resource.get("subscriber", {})
    email = subscriber.get("email_address")
    if not email:
        return
    user = User.objects.filter(email=email).first()
    if not user:
        return
    subscription, _ = Subscription.objects.get_or_create(user=user)
    subscription.plan = "premium"
    subscription.active = active
    subscription.start_date = timezone.now()
    subscription.end_date = None if active else timezone.now()
    subscription.save()

    if resource.get("billing_info"):
        last_payment = resource["billing_info"].get("last_payment")
        if last_payment:
            Payment.objects.create(
                user=user,
                provider="paypal",
                amount=last_payment["amount"]["value"],
                status="completed" if active else "failed",
                transaction_id=last_payment["transaction_id"],
                created_at=datetime.fromisoformat(last_payment["time"].replace("Z", "+00:00")),
            )
