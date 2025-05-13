from django.contrib import admin

from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "total_amount",
        "created_at",
        "updated_at",
    )

class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quantity",
        "price_at_order_time",
        "subtotal",
        "created_at",
        "updated_at"
    )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
