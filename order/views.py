from rest_framework import generics

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


class OrderCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        created_at = self.request.query_params.get("created_at")
        status = self.request.query_params.get("status")

        if created_at:
            try:
                # Filter by date with format yyyy-mm-dd
                queryset = queryset.filter(created_at__date=created_at)
            except ValueError:
                # If the date format is invalid, return empty queryset
                return Order.objects.none()

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        order_id = self.request.query_params.get("order_id")
        menu_id = self.request.query_params.get("menu_id")
        created_at = self.request.query_params.get("created_at")

        if order_id:
            queryset = queryset.filter(order_id=order_id)

        if menu_id:
            queryset = queryset.filter(menu_id=menu_id)

        if created_at:
            try:
                # Filter by date with format yyyy-mm-dd
                queryset = queryset.filter(created_at__date=created_at)
            except ValueError:
                # If the date format is invalid, return empty queryset
                return OrderItem.objects.none()

        return queryset


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
