from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from menu.models import Menu
from shared.models import BaseModel


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"

    status = models.CharField(
        max_length=10, choices=OrderStatus.choices, default=OrderStatus.UNPAID
    )
    order_items = models.ManyToManyField(Menu, through="OrderItem")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}. Status: {self.status}"


class OrderItem(BaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)


# Signal handlers to update Order total_amount when OrderItem is created or updated
@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    """
    Signal handler to update the order's total_amount when an OrderItem is created or updated
    """
    order = instance.order_id
    order_items = OrderItem.objects.filter(order_id=order)
    total = sum(item.subtotal for item in order_items)
    order.total_amount = total
    order.save()


# Signal handler to update Order total_amount when an OrderItem is deleted
@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the order's total_amount when an OrderItem is deleted
    """
    order = instance.order_id
    order_items = OrderItem.objects.filter(order_id=order)
    if order_items.exists():
        total = sum(item.subtotal for item in order_items)
    else:
        total = 0
    order.total_amount = total
    order.save()
