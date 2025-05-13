from django.urls import path

from .views import OrderCreateView, OrderItemCreateView, OrderDetailView, OrderItemDetailView

urlpatterns = [
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<str:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("order-items/", OrderItemCreateView.as_view(), name="order-item-create"),
    path("order-items/<str:pk>/", OrderItemDetailView.as_view(), name="order-item-detail"),
]
    