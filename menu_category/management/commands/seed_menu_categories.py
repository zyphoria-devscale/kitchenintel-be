from django.core.management.base import BaseCommand
from menu_category.models import MenuCategory
from django.db import transaction
from menu_category.seed.menu_category_data import parent_category_data, child_category_data

class Command(BaseCommand):
    help = "Seed Menu Categories with parent-child relationships"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        parents = parent_category_data

        children = child_category_data

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