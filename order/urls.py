from django.urls import path

from .views import OrderWithItemsCreateView, OrderWithItemsDetailView

urlpatterns = [
    path(
        "orders-with-items/",
        OrderWithItemsCreateView.as_view(),
        name="order-with-items-create",
    ),
    path(
        "orders-with-items/<str:pk>/",
        OrderWithItemsDetailView.as_view(),
        name="order-with-items-detail",
    ),
]
