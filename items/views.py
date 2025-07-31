import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path
from django.views import View

from config.settings import env
from items.models import Item

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


class CreateCheckoutSessionView(View):
    def get(self, request, id, *args, **kwargs):
        item = get_object_or_404(Item, id=id)

        domain = request.build_absolute_uri("/")[:-1]
        print(domain)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
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


urlpatterns = [
    path("item/<id>/", ItemDetailView.as_view(), name="item_detail"),
    path(
        "buy/<id>/", CreateCheckoutSessionView.as_view(), name="create_checkout_session"
    ),
]
