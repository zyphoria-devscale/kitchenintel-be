from rest_framework import serializers
from shared.utils import asia_jakarta_time

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = "__all__"
        
    def get_created_at(self, obj):
        return asia_jakarta_time(obj.created_at).strftime('%Y-%m-%d %H:%M:%S')
        
    def get_updated_at(self, obj):
        return asia_jakarta_time(obj.updated_at).strftime('%Y-%m-%d %H:%M:%S')


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order_id=obj.id)
        return OrderItemSerializer(order_items, many=True).data
        
    def get_created_at(self, obj):
        return asia_jakarta_time(obj.created_at).strftime('%Y-%m-%d %H:%M:%S')
        
    def get_updated_at(self, obj):
        return asia_jakarta_time(obj.updated_at).strftime('%Y-%m-%d %H:%M:%S')
