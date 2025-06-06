from django.urls import path

from .views import (
    MonthlyDashboardDetailView,
    MonthlyDashboardListView,
    WeeklyDashboardDetailView,
    WeeklyDashboardListView,
    GeneratePastData
)

urlpatterns = [
    path(
        "weekly-dashboard/",
        WeeklyDashboardListView.as_view(),
        name="weekly-dashboard-list",
    ),
    path(
        "weekly-dashboard/<str:pk>/",
        WeeklyDashboardDetailView.as_view(),
        name="weekly-dashboard-detail",
    ),
    path(
        "monthly-dashboard/",
        MonthlyDashboardListView.as_view(),
        name="monthly-dashboard-list",
    ),
    path(
        "monthly-dashboard/<str:pk>/",
        MonthlyDashboardDetailView.as_view(),
        name="monthly-dashboard-detail",
    ),
    path('generate-data/', GeneratePastData.as_view(), name='generate-past-data-api'),
]
