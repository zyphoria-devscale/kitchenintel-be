from django.db import models
from shared.models import BaseModel

# Create your models here.
class Menu(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey("menu_category.MenuCategory", on_delete=models.RESTRICT)
    is_recommend = models.BooleanField(default=False)
