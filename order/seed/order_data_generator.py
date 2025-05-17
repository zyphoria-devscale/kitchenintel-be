"""
Order data generator for seed data.
This module generates order data for a specified date range based on defined patterns.
"""

import random
import datetime
from .order_patterns import (
    WEEKDAY_PATTERN, 
    WEEKEND_PATTERN, 
    SPECIAL_DAYS, 
    STATUS_DISTRIBUTION,
    NOTES_TEMPLATES,
    CUSTOMER_NAMES
)

def is_weekend(date):
    """Check if the given date is a weekend (Saturday or Sunday)."""
    return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

def get_day_pattern(date):
    """Get the appropriate pattern for the given date."""
    date_str = date.strftime("%Y-%m-%d")
    
    # Check if it's a special day
    if date_str in SPECIAL_DAYS:
        # Use the appropriate base pattern with modifications
        if is_weekend(date):
            pattern = WEEKEND_PATTERN.copy()
        else:
            pattern = WEEKDAY_PATTERN.copy()
        
        # Apply special day multiplier
        for time_slot in pattern:
            pattern[time_slot]["order_frequency"] *= SPECIAL_DAYS[date_str]["order_multiplier"]
            
        return pattern, SPECIAL_DAYS[date_str]
    
    # Regular day pattern
    if is_weekend(date):
        return WEEKEND_PATTERN, None
    else:
        return WEEKDAY_PATTERN, None

def generate_random_time(hour_start, hour_end):
    """Generate a random time between the specified hours."""
    hour = random.randint(hour_start, hour_end - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return hour, minute, second

def generate_order_items(popular_items, avg_items, all_menu_items):
    """Generate a random number of order items."""
    # Determine number of items in this order
    num_items = max(1, int(random.normalvariate(avg_items, 0.7)))
    
    # 70% chance to include popular items, 30% chance for any menu item
    items = []
    for _ in range(num_items):
        if random.random() < 0.7 and popular_items:
            menu_title = random.choice(popular_items)
        else:
            menu_title = random.choice(all_menu_items)
            
        # Generate quantity (usually 1-3, occasionally more)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.6, 0.25, 0.1, 0.03, 0.02])[0]
        
        # Generate notes (80% chance of no notes)
        notes = random.choices(NOTES_TEMPLATES, weights=[0.8] + [0.02] * (len(NOTES_TEMPLATES) - 1))[0]
        
        items.append({
            "menu_title": menu_title,
            "quantity": quantity,
            "notes": notes
        })
    
    return items

def generate_orders_for_date(date, all_menu_items):
    """Generate orders for a specific date based on patterns."""
    pattern, special_day = get_day_pattern(date)
    orders_data = {}
    
    # Generate orders for each time slot in the pattern
    for slot_name, slot_data in pattern.items():
        start_hour, end_hour = slot_data["time_range"]
        num_orders = int(random.normalvariate(slot_data["order_frequency"], slot_data["order_frequency"] * 0.2))
        
        # Generate each order
        for _ in range(num_orders):
            # Generate random time within this slot
            hour, minute, second = generate_random_time(start_hour, end_hour)
            timestamp = datetime.datetime(
                date.year, date.month, date.day, hour, minute, second
            )
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            # Determine order status based on distribution
            status = random.choices(
                list(STATUS_DISTRIBUTION.keys()), 
                weights=list(STATUS_DISTRIBUTION.values())
            )[0]
            
            # Generate order items
            popular_items = slot_data["popular_items"]
            # Add special items if it's a special day
            if special_day and "special_items" in special_day:
                popular_items = popular_items + special_day["special_items"]
                
            order_items = generate_order_items(
                popular_items, 
                slot_data["avg_items_per_order"],
                all_menu_items
            )
            
            # Create the order
            if timestamp_str not in orders_data:
                orders_data[timestamp_str] = []
                
            orders_data[timestamp_str].append({
                "status": status,
                "order_items": order_items,
                "customer_name": random.choice(CUSTOMER_NAMES)
            })
    
    return orders_data

def generate_orders_for_month(year, month, all_menu_items):
    """Generate orders for an entire month."""
    # Determine the number of days in the month
    if month == 2:
        days_in_month = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
    elif month in [4, 6, 9, 11]:
        days_in_month = 30
    else:
        days_in_month = 31
    
    all_orders = {}
    
    # Generate orders for each day
    for day in range(1, days_in_month + 1):
        date = datetime.date(year, month, day)
        daily_orders = generate_orders_for_date(date, all_menu_items)
        all_orders.update(daily_orders)
    
    return all_orders

def get_all_menu_titles():
    """Get all menu titles from the menu data."""
    try:
        from menu.seed.menu_data import data
        return [item["title"] for item in data]
    except ImportError as e:
        raise ImportError(f"Menu data not found. Error: {str(e)}") 

def generate_may_2025_orders():
    """Generate orders for May 2025."""
    all_menu_items = get_all_menu_titles()
    return generate_orders_for_month(2025, 5, all_menu_items)
