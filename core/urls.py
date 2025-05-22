from core.logout import logout_view
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("menu_category.urls")),
    path("api/", include("menu.urls")),
    path("api/", include("order.urls")),
    path("api/", include("dashboard.urls")),
    path("api/login", obtain_auth_token, name="api_token_auth"),
    path("api/logout", logout_view, name="api_logout")
]
