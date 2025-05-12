from rest_framework import serializers

from .models import MenuCategory


class MenuCategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.filter(parent_id__isnull=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MenuCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're updating an existing instance, exclude it from parent options
        instance = kwargs.get("instance")
        if instance:
            self.fields["parent_id"].queryset = self.fields[
                "parent_id"
            ].queryset.exclude(pk=instance.pk)
