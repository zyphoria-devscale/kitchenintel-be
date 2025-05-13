from django.db import models

from shared.models import BaseModel


# Create your models here.
class MenuCategory(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent_id = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        db_table = "menu_categories"
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"

    def __str__(self):
        return self.title
