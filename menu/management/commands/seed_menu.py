from django.core.management.base import BaseCommand
from menu.models import Menu
from menu_category.models import MenuCategory
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from menu.seed.menu_data import data

class Command(BaseCommand):
    help = "Seed Menus"

    def get_category_id(self, category_title):
        try:
            category = MenuCategory.objects.get(title=category_title)
            return category
        except ObjectDoesNotExist:
            self.stdout.write(self.style.WARNING(f"Category '{category_title}' not found"))
            return None

    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            # Define menu data with category titles instead of direct IDs
            menu_data = data
            
            # Process menu data and create menu objects
            menus = []
            for menu_item in menu_data:
                # Extract category title and get its ID
                category_title = menu_item.pop("category")
                category_id = self.get_category_id(category_title)
                
                if category_id:
                    # Add category ID to menu item data
                    menu_item["category_id"] = category_id
                    
                    # Check if menu already exists
                    existing_menu = Menu.objects.filter(title=menu_item["title"]).first()
                    if existing_menu:
                        self.stdout.write(self.style.WARNING(f"Menu '{menu_item['title']}' already exists, skipping"))
                    else:
                        menus.append(Menu(**menu_item))
                        self.stdout.write(self.style.SUCCESS(f"Prepared menu: {menu_item['title']}"))

            # Bulk create menus if any valid menus exist
            if menus:
                Menu.objects.bulk_create(menus)
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(menus)} menus"))
            else:
                self.stdout.write(self.style.WARNING("No menus were created"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding menus: {str(e)}"))
            # The transaction.atomic decorator will handle the rollback
