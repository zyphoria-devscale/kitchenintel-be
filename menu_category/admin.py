from django import forms
from django.contrib import admin

from .models import MenuCategory


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter parent_id choices to only show categories where parent_id is null
        self.fields["parent_id"].queryset = MenuCategory.objects.filter(
            parent_id__isnull=True
        )

        # If we're editing an existing object, exclude it from the parent options
        if self.instance.pk:
            self.fields["parent_id"].queryset = self.fields[
                "parent_id"
            ].queryset.exclude(pk=self.instance.pk)


class MenuCategoryAdmin(admin.ModelAdmin):
    form = MenuCategoryForm
    list_display = ("title", "parent_id", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("parent_id",)


# Register the model with the custom admin
admin.site.register(MenuCategory, MenuCategoryAdmin)
