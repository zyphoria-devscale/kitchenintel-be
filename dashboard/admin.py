from django.contrib import admin

from .models import Dashboard, Graph


# Register your models here.
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("type_dashboard", "created_at")
    list_filter = ("type_dashboard",)
    search_fields = ("type_dashboard",)


class GraphAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "dashboard")
    list_filter = ("title", "dashboard")
    search_fields = ("title", "dashboard")


admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Graph, GraphAdmin)
