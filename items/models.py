from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from items.constants import ITEM_PRICE_CURRENCIES


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.IntegerField(choices=ITEM_PRICE_CURRENCIES)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField("items.Item")
    discount = models.ForeignKey(
        "items.Discount", on_delete=models.SET_NULL, null=True, blank=True
    )
    tax = models.ForeignKey(
        "items.Tax", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return str(self.id)


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent_off = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    stripe_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stripe_id = models.CharField(max_length=50, blank=True)
    inclusive = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"

    def __str__(self):
        return self.name
