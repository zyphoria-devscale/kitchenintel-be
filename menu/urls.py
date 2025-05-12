from django.urls import path   

from .views import MenuCreateView, MenuDetailView

urlpatterns = [
    path("menus/", MenuCreateView.as_view(), name="menu-list-create"),
    path("menus/<str:pk>/", MenuDetailView.as_view(), name="menu-detail"),
]
