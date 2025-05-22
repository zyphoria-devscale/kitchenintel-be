from datetime import date
from typing import Any, List, Tuple

from django.db.models import F
from django.db.models.functions import TruncDate
from order.models import OrderItem
from shared.utils import asia_jakarta_time


def get_order_details(from_date: date, to_date: date) -> List[Tuple[Any, ...]]:
    """
    Fetch order details as a list of tuples.

    Each tuple contains:
    (order_no, title, category_title, quantity, price_at_order_time, subtotal, notes, order_date, created_at)
    """
    queryset = (
        OrderItem.objects.select_related(
            "order_id",
            "menu_id",
            "menu_id__category_id",
            "menu_id__category_id__parent_id",
        )
        .annotate(
            order_no=F("order_id__id"),
            title=F("menu_id__title"),
            category_title=F("menu_id__category_id__parent_id__title"),
            order_date_format=TruncDate("order_id__created_at"),
            order_date=F("order_id__created_at"),
            menu_name=F("menu_id__title"),
            category=F("menu_id__category_id__parent_id__title"),
        )
        .filter(order_date_format__gte=from_date, order_date_format__lte=to_date)
        .values_list(
            "order_no",
            "menu_name",
            "category",
            "quantity",
            "price_at_order_time",
            "subtotal",
            "notes",
            "order_date",
        )
    )
    result = []
    for order in queryset:
        *others, order_date = order
        order_date = asia_jakarta_time(order_date)
        result.append((*others, order_date))

    return result
