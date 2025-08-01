from django.contrib import admin

from items.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "currency")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "discount", "tax")
    readonly_fields = ("created_at",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent_off", "stripe_id")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage", "stripe_id", "inclusive")
