from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order_id=obj.id)
        return OrderItemSerializer(order_items, many=True).data
