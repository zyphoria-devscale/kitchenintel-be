from rest_framework import serializers

from .models import Menu
from menu_category.models import MenuCategory


class MenuSerializer(serializers.ModelSerializer):
    # only show child category
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.filter(parent_id__isnull=False),
    )
    class Meta:
        model = Menu
        fields = "__all__"