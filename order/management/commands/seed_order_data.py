from django.core.management.base import BaseCommand
from order.models import Order, OrderItem
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from menu.models import Menu
from shared.utils import convert_to_utc

from order.seed.order_data_generator import generate_may_2025_orders

class Command(BaseCommand):
    help = "Seed Order Data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing order data before seeding'
        )

    def get_menu_by_title(self, menu_title):
        try:
            menu = Menu.objects.get(title=menu_title)
            return menu
        except ObjectDoesNotExist:
            self.stdout.write(self.style.WARNING(f"Menu '{menu_title}' not found"))
            return None
    
    def update_utc_timestamps(self, order_id, utc_dt):
        Order.objects.filter(id=order_id).update(
            created_at=utc_dt,
            updated_at=utc_dt
        )
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding order data...")
        
        # Clear existing data if requested
        if kwargs.get('clear'):
            self.stdout.write("Clearing existing order data...")
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Existing order data cleared"))
        
        # Generate data for May 2025
        data = generate_may_2025_orders()
        
        self.stdout.write(f"Generated {len(data)} timestamps with orders")

        orders_data = []
        order_items_data = []

        try:
            for order_date, orders in data.items():
                for order in orders:
                    total_amount = 0

                for order_item in order["order_items"]:
                    menu = self.get_menu_by_title(order_item["menu_title"])
                    subtotal = menu.price * order_item["quantity"]
                    total_amount += subtotal
                    
                    order_item["menu_id"] = menu.id
                    order_item["price_at_order_time"] = menu.price
                    order_item["subtotal"] = subtotal
                    order_item["created_at"] = order_date
                    order_item["updated_at"] = order_date
                    order_items_data.append(order_item)
                
                orders_data.append({
                    "status": order["status"],
                    "customer_name": order["customer_name"],
                    "total_amount": total_amount,
                    "created_at": order_date,
                    "updated_at": order_date,
                })
        
            if orders_data:
                orders = []
                order_map = {}  # Dictionary to map created_at strings to Order objects
                
                for order_dict in orders_data:
                    # Parse the string to datetime and convert from UTC+7 to UTC
                    date_str = order_dict["created_at"]
                    utc_dt = convert_to_utc(date_str)

                    # Create the order (this will use auto timestamps)
                    order = Order.objects.create(
                        status=order_dict["status"],
                        total_amount=order_dict["total_amount"],
                        customer_name=order_dict["customer_name"]
                    )
                    
                    # Update the timestamps directly in the database with UTC time
                    self.update_utc_timestamps(order.id, utc_dt)
                    
                    # Refresh the instance to get the updated values
                    order.refresh_from_db()
                    
                    # Store the order in our list and map
                    orders.append(order)
                    order_map[order_dict["created_at"]] = order
                
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(orders)} orders"))
            else:
                self.stdout.write(self.style.WARNING("No orders were created"))

            if order_items_data:
                order_items = []
                for item_dict in order_items_data:
                    # Use the order_map to get the Order instance by date string
                    order = order_map[item_dict["created_at"]]
                    menu = Menu.objects.get(id=item_dict["menu_id"])
                    
                    # Parse the string to datetime and convert from UTC+7 to UTC
                    date_str = item_dict["created_at"]
                    utc_dt = convert_to_utc(date_str)
                    
                    # Create the OrderItem
                    order_item = OrderItem.objects.create(
                        order_id=order,
                        menu_id=menu,
                        quantity=item_dict["quantity"],
                        price_at_order_time=item_dict["price_at_order_time"],
                        subtotal=item_dict["subtotal"],
                        notes=item_dict.get("notes", "")
                    )
                    
                    # Update timestamps directly in the database with UTC time
                    self.update_utc_timestamps(order_item.id, utc_dt)
                    
                    # Refresh to get updated values
                    order_item.refresh_from_db()
                    
                    order_items.append(order_item)
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(order_items)} order items"))
            else:
                self.stdout.write(self.style.WARNING("No order items were created"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding order data: {str(e)}"))
        
        