from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    price_at_order_time = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def create(self, validated_data):
        # Get the menu item to retrieve its price
        menu = validated_data["menu_id"]

        # Set price_at_order_time from the menu's price
        validated_data["price_at_order_time"] = menu.price

        # Calculate subtotal based on quantity and price
        quantity = validated_data.get("quantity", 1)
        validated_data["subtotal"] = quantity * menu.price

        # Create the order item with the updated data
        order_item = OrderItem.objects.create(**validated_data)

        return order_item

    def update(self, instance, validated_data):
        # Check if quantity is being updated
        if "quantity" in validated_data:
            # Recalculate subtotal based on the new quantity and existing price
            new_quantity = validated_data["quantity"]
            validated_data["subtotal"] = new_quantity * instance.price_at_order_time

        # If menu_id is being updated, update price_at_order_time and recalculate subtotal
        if "menu_id" in validated_data:
            menu = validated_data["menu_id"]
            validated_data["price_at_order_time"] = menu.price
            quantity = validated_data.get("quantity", instance.quantity)
            validated_data["subtotal"] = quantity * menu.price

        # Update the order item
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order_id=obj.id)
        return OrderItemSerializer(order_items, many=True).data

    def create(self, validated_data):
        validated_data["total_amount"] = 0
        order = Order.objects.create(**validated_data)
        return order
