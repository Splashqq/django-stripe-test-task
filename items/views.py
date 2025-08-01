import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path
from django.views import View

from config.settings import env
from items.models import Item, Order

stripe.api_key = env("STRIPE_SECRET_KEY")


class ItemDetailView(View):
    template_name = "item_detail.html"

    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, id=id)
        context = {
            "item": item,
            "stripe_public_key": env("STRIPE_PUBLIC_KEY"),
        }
        return render(request, self.template_name, context)


class BuyItem(View):
    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, id=id)

        domain = request.build_absolute_uri("/")[:-1]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": item.currency,
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=domain,
            cancel_url=domain + f"/item/{id}/",
        )

        return JsonResponse({"session_id": session.id})


class OrderDetailView(View):
    template_name = "order_detail.html"

    def get(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id)

        subtotal = sum(item.price for item in order.items.all())
        discount_amount = (
            round(subtotal * (order.discount.percent_off / 100), 2)
            if order.discount
            else 0
        )
        tax_amount = (
            round(subtotal * (order.tax.percentage / 100), 2)
            if order.tax and not order.tax.inclusive
            else 0
        )

        order.total_price = subtotal - discount_amount + tax_amount

        context = {
            "order": order,
            "stripe_public_key": env("STRIPE_PUBLIC_KEY"),
        }

        return render(request, self.template_name, context)


class BuyOrder(View):
    def get(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        line_items = []

        domain = request.build_absolute_uri("/")[:-1]

        currency = order.items.first().get_currency_display()

        for item in order.items.all():
            line_items.append(
                {
                    "price_data": {
                        "currency": item.get_currency_display(),
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                }
            )

        session_kwargs = {
            "currency": currency,
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": domain,
            "cancel_url": domain + f"/order/{id}/",
        }

        if order.discount:
            session_kwargs["discounts"] = [{"coupon": order.discount.stripe_id}]

        if order.tax:
            session_kwargs["automatic_tax"] = {"enabled": True}

        session = stripe.checkout.Session.create(**session_kwargs)

        return JsonResponse({"session_id": session.id})


urlpatterns = [
    path("item/<id>/", ItemDetailView.as_view(), name="item_detail"),
    path("buy/<id>/", BuyItem.as_view(), name="buy_item"),
    path("order/<id>/", OrderDetailView.as_view(), name="order_detail"),
    path("buy_order/<id>/", BuyOrder.as_view(), name="buy_order"),
]
