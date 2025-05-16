from rest_framework import generics

from .models import Order
from .serializers import OrderWithItemsSerializer


class OrderWithItemsCreateView(generics.ListCreateAPIView):
    serializer_class = OrderWithItemsSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        created_at = self.request.query_params.get("created_at")
        order_status = self.request.query_params.get("status")

        if created_at:
            try:
                # Filter by date with format yyyy-mm-dd
                queryset = queryset.filter(created_at__date=created_at)
            except ValueError:
                # If the date format is invalid, return empty queryset
                return Order.objects.none()

        if order_status:
            queryset = queryset.filter(status=order_status)

        return queryset


class OrderWithItemsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWithItemsSerializer
