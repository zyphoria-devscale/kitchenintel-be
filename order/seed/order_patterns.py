"""
Order patterns for seed data generation.
This file contains patterns that define how orders are distributed throughout the day.
"""

# Define different order patterns for different day types
WEEKDAY_PATTERN = {
    # Morning rush (7:00 AM - 10:00 AM)
    "morning": {
        "time_range": (7, 10),  # Hours (7:00 - 10:00)
        "order_frequency": 10,  # Average number of orders per hour
        "popular_items": [
            "Hot Cappuccino", "Croissant with Jam", "Roti Bakar Coklat",
            "Apple Pie", "Vanilla Milkshake"
        ],
        "avg_items_per_order": 1.5,  # Average number of items per order
    },
    # Lunch rush (11:00 AM - 2:00 PM)
    "lunch": {
        "time_range": (11, 14),
        "order_frequency": 25,  # Busier during lunch
        "popular_items": [
            "Nasi Goreng Special", "Beef Rendang", "Chicken Teriyaki",
            "Bakso", "Gado-Gado Salad", "Pad Thai", "Mie Goreng Jawa"
        ],
        "avg_items_per_order": 2.2,
    },
    # Afternoon (2:00 PM - 5:00 PM)
    "afternoon": {
        "time_range": (14, 17),
        "order_frequency": 8,
        "popular_items": [
            "Ice Thai Tea", "Es Cendol", "Matcha Smoothie", 
            "Apple Pie", "Chocolate Lava Cake", "Es Campur", "Tiramisu"
        ],
        "avg_items_per_order": 1.8,
    },
    # Dinner rush (5:00 PM - 9:00 PM)
    "dinner": {
        "time_range": (17, 21),
        "order_frequency": 20,
        "popular_items": [
            "Beef Rendang", "Korean Fried Chicken", "Grilled Chicken Steak",
            "BBQ Pork Ribs", "Spaghetti Carbonara", "Beef Lasagna",
            "Tom Yum Soup", "Ramen Shoyu"
        ],
        "avg_items_per_order": 2.5,
    },
}

WEEKEND_PATTERN = {
    # Morning (8:00 AM - 11:00 AM)
    "morning": {
        "time_range": (8, 11),
        "order_frequency": 15,  # More orders on weekend mornings
        "popular_items": [
            "Hot Cappuccino", "Croissant with Jam", "Roti Bakar Coklat",
            "Apple Pie", "Vanilla Milkshake", "Mushroom Soup"
        ],
        "avg_items_per_order": 2.0,
    },
    # Lunch rush (11:00 AM - 3:00 PM)
    "lunch": {
        "time_range": (11, 15),  # Extended lunch hours on weekends
        "order_frequency": 30,
        "popular_items": [
            "Nasi Goreng Special", "Beef Rendang", "Chicken Teriyaki",
            "Bakso", "Gado-Gado Salad", "Pad Thai", "Mie Goreng Jawa",
            "Satay Ayam", "Tom Yum Soup"
        ],
        "avg_items_per_order": 2.5,
    },
    # Afternoon (3:00 PM - 6:00 PM)
    "afternoon": {
        "time_range": (15, 18),
        "order_frequency": 12,
        "popular_items": [
            "Ice Thai Tea", "Es Cendol", "Matcha Smoothie", 
            "Apple Pie", "Chocolate Lava Cake", "Ice Cream Sundae",
            "Es Campur", "Tiramisu", "Strawberry Smoothie"
        ],
        "avg_items_per_order": 2.0,
    },
    # Dinner rush (6:00 PM - 10:00 PM)
    "dinner": {
        "time_range": (18, 22),
        "order_frequency": 25,
        "popular_items": [
            "Beef Rendang", "Korean Fried Chicken", "Grilled Chicken Steak",
            "BBQ Pork Ribs", "Spaghetti Carbonara", "Beef Lasagna",
            "Tom Yum Soup", "Ramen Shoyu", "Holiday Roast Turkey"
        ],
        "avg_items_per_order": 3.0,  # More items per order on weekend dinners
    },
    # Late night (10:00 PM - 12:00 AM)
    "late_night": {
        "time_range": (22, 24),
        "order_frequency": 8,
        "popular_items": [
            "Mie Goreng Jawa", "Chicken Quesadilla", "Classic Cheeseburger",
            "Ice Cream Sundae", "Strawberry Smoothie", "Vanilla Milkshake"
        ],
        "avg_items_per_order": 1.8,
    },
}

# Special days with different patterns (e.g., holidays, promotions)
SPECIAL_DAYS = {
    # Example: Mother's Day (May 12, 2025)
    "2025-05-12": {
        "name": "Mother's Day",
        "order_multiplier": 1.5,  # 50% more orders than usual
        "special_items": ["Holiday Roast Turkey", "Chocolate Lava Cake", "Strawberry Smoothie", "Limited Time Lamb Chops"],
    },
    # Example: End of Month Promotion (May 31, 2025)
    "2025-05-31": {
        "name": "Month-End Promotion",
        "order_multiplier": 1.3,
        "special_items": ["Beef Rendang", "Korean Fried Chicken", "Ice Cream Sundae", "Weekly Chef Special"],
    }
}

# Order status distribution
STATUS_DISTRIBUTION = {
    "PAID": 0.95,      # 95% of orders are paid
    "UNPAID": 0.05  # 5% of orders are cancelled
}

# Notes templates for order items
NOTES_TEMPLATES = [
    "",  # Empty note (most common)
    "Extra spicy",
    "Less sugar",
    "No onions",
    "Extra sauce",
    "Well done",
    "Medium rare",
    "Extra noodle",
    "No cilantro",
    "Gluten-free if possible",
    "Extra cheese"
]
