from django.db import transaction
from menu.models import Menu
from rest_framework import serializers
from shared.utils import format_customer_name

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""

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


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating order items within an order"""

    menu_id = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ["menu_id", "quantity", "notes"]


class OrderWithItemsSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating an order with its items in a single request"""

    items = OrderItemCreateSerializer(many=True, write_only=True, required=False)
    order_items = serializers.SerializerMethodField(read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["total_amount"]

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order_id=obj.id)
        return OrderItemSerializer(order_items, many=True).data

    def validate_create(self, attrs):
        """Validate that items are provided when creating an order"""
        # Check if this is a create operation (no instance exists yet)
        if not hasattr(self, "instance") or self.instance is None:
            # For creation, items are required
            if "items" not in attrs or not attrs["items"]:
                raise serializers.ValidationError(
                    {
                        "items": "At least one order item is required when creating an order."
                    }
                )
        return attrs

    def validate(self, attrs):
        """Perform validation that applies to both create and update"""
        # First run the standard validation
        attrs = super().validate(attrs)
        # Then run create-specific validation
        return self.validate_create(attrs)

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        customer_name = format_customer_name(validated_data["customer_name"])
        validated_data["customer_name"] = customer_name

        # Create order with initial total_amount=0
        order = Order.objects.create(total_amount=0, **validated_data)

        # Create order items (items_data will never be empty due to validation)
        self._create_or_update_items(order, items_data)

        # Refresh the order to get the updated total
        order.refresh_from_db()

        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        # Update order fields (like status)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If items were provided, update them
        if items_data is not None:
            # Option: Clear existing items and create new ones
            # This is a "replace" approach rather than "merge"
            OrderItem.objects.filter(order_id=instance).delete()
            self._create_or_update_items(instance, items_data)

        # Refresh to get updated total
        instance.refresh_from_db()

        return instance

    def _create_or_update_items(self, order, items_data):
        """Helper method to create order items"""
        for item_data in items_data:
            menu = item_data["menu_id"]
            quantity = item_data.get("quantity", 1)
            notes = item_data.get("notes", None)

            # Calculate price and subtotal
            price = menu.price
            subtotal = price * quantity

            # Create the order item
            OrderItem.objects.create(
                order_id=order,
                menu_id=menu,
                quantity=quantity,
                price_at_order_time=price,
                subtotal=subtotal,
                notes=notes,
            )
