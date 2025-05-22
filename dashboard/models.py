from django.db import models
from shared.models import BaseModel

WEEKLY_DASHBOARD = "weekly"
MONTHLY_DASHBOARD = "monthly"

DASHBOARD_TYPE_CHOICES = (
    (WEEKLY_DASHBOARD, "Weekly"),
    (MONTHLY_DASHBOARD, "Monthly"),
)


# Create your models here.
class Dashboard(BaseModel):
    type_dashboard = models.CharField(max_length=100, choices=DASHBOARD_TYPE_CHOICES)
    insight = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_dashboard}"


class Graph(BaseModel):
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.SET_NULL, null=True, blank=True
    )
    url = models.URLField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    raw_data = models.JSONField(null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
