from django.urls import path

from .views import MenuCategoryCreateView, MenuCategoryDetailView

urlpatterns = [
    path(
        "menu-categories/",
        MenuCategoryCreateView.as_view(),
        name="menu-category-list-create",
    ),
    path(
        "menu-categories/<str:pk>/",
        MenuCategoryDetailView.as_view(),
        name="menu-category-detail",
    ),
]
