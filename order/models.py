from django.db import models
from shared.models import BaseModel
from menu.models import Menu
from django.core.validators import MinValueValidator

class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"
    
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.UNPAID)
    order_items = models.ManyToManyField(Menu, through='OrderItem')
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
    

