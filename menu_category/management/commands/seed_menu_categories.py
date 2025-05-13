from django.core.management.base import BaseCommand
from menu_category.models import MenuCategory
from django.db import transaction

class Command(BaseCommand):
    help = "Seed Menu Categories with parent-child relationships"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        parents = {
            'cat001': {'title': 'Food', 'description': 'Main food menu'},
            'cat002': {'title': 'Drinks', 'description': 'Beverage options'},
            'cat003': {'title': 'Desserts', 'description': 'Sweet dishes'},
            'cat004': {'title': 'Appetizers', 'description': 'Starters and light snacks'},
            'cat005': {'title': 'Specials', 'description': 'Seasonal or chef\'s specials'},
        }

        children = {
            'cat001': [
                {'title': 'Rice Dishes', 'description': 'Meals served with rice'},
                {'title': 'Noodle Dishes', 'description': 'Meals with various types of noodles'},
                {'title': 'Grilled Items', 'description': 'Grilled meats and vegetables'},
            ],
            'cat002': [
                {'title': 'Hot Drinks', 'description': 'Coffee, tea, and more'},
                {'title': 'Cold Drinks', 'description': 'Iced beverages and soft drinks'},
                {'title': 'Smoothies', 'description': 'Fruit and yogurt-based drinks'},
            ],
            'cat003': [
                {'title': 'Cakes', 'description': 'Various cake options'},
                {'title': 'Ice Cream', 'description': 'Classic and custom flavors'},
                {'title': 'Pastries', 'description': 'Tarts, croissants, and more'},
            ],
            'cat004': [
                {'title': 'Finger Food', 'description': 'Bite-sized snacks'},
                {'title': 'Soups', 'description': 'Warm and hearty soups'},
                {'title': 'Salads', 'description': 'Fresh and healthy salads'},
            ],
            'cat005': [
                {'title': 'Weekly Specials', 'description': 'Updated every week'},
                {'title': 'Holiday Specials', 'description': 'Festive themed dishes'},
                {'title': 'Limited Time Offers', 'description': 'Time-sensitive dishes'},
            ],
        }

        self.stdout.write("Seeding parent categories...")
        parent_objs = {}

        for key, data in parents.items():
            obj, created = MenuCategory.objects.get_or_create(
                title=data["title"],
                defaults={"description": data["description"]}
            )
            parent_objs[key] = obj
            self.stdout.write(
                self.style.SUCCESS(f"{'Created' if created else 'Exists'} parent: {obj.title}")
            )

        self.stdout.write("Seeding child categories...")
        for parent_key, child_list in children.items():
            parent = parent_objs[parent_key]
            for child_data in child_list:
                child, created = MenuCategory.objects.get_or_create(
                    title=child_data["title"],
                    parent_id=parent,
                    defaults={"description": child_data["description"]}
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{'Created' if created else 'Exists'} child: {child.title} → parent: {parent.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("✅ Menu category seed complete."))