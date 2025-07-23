import os
import stripe
from flask import Blueprint, request, redirect

stripe.api_key = os.getenv("STRIPE_SECRET")
DOMAIN = os.getenv("DOMAIN")

stripe_bp = Blueprint("stripe", __name__)

@stripe_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 5000,  # $50.00
                        "product_data": {
                            "name": "Консультация по иммиграции",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=DOMAIN + "/success",
            cancel_url=DOMAIN + "/cancel",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400
