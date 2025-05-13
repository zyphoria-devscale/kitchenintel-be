from django.contrib import admin
from .models import Menu

# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "is_recommended", "category_id")
    search_fields = ("title",)
    list_filter = ("category_id",)

admin.site.register(Menu, MenuAdmin)