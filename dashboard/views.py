from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from .models import Dashboard
from .serializers import DashboardWithGraphsSerializer


class WeeklyDashboardListView(generics.ListAPIView):
    """API endpoint for listing weekly dashboards.
    
    Returns the 4 most recent weekly dashboards with their associated graphs.
    """
    serializer_class = DashboardWithGraphsSerializer
    
    def get_queryset(self):
        """Return optimized queryset for weekly dashboards."""
        return Dashboard.objects.filter(type_dashboard="weekly").order_by(
            "-created_at"
        )[:4]
        
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """Override list method to add caching."""
        return super().list(request, *args, **kwargs)


class MonthlyDashboardListView(generics.ListAPIView):
    """API endpoint for listing monthly dashboards.
    
    Returns the 3 most recent monthly dashboards with their associated graphs.
    """
    serializer_class = DashboardWithGraphsSerializer
    
    def get_queryset(self):
        """Return optimized queryset for monthly dashboards."""
        return Dashboard.objects.filter(type_dashboard="monthly").order_by(
            "-created_at"
        )[:3]
        
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def list(self, request, *args, **kwargs):
        """Override list method to add caching."""
        return super().list(request, *args, **kwargs)


class WeeklyDashboardDetailView(generics.RetrieveAPIView):
    """API endpoint for retrieving a specific weekly dashboard.
    
    Returns a single weekly dashboard with its associated graphs.
    """
    serializer_class = DashboardWithGraphsSerializer
    
    def get_queryset(self):
        """Return optimized queryset for weekly dashboards."""
        return Dashboard.objects.filter(type_dashboard="weekly")
        
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add caching."""
        return super().retrieve(request, *args, **kwargs)


class MonthlyDashboardDetailView(generics.RetrieveAPIView):
    """API endpoint for retrieving a specific monthly dashboard.
    
    Returns a single monthly dashboard with its associated graphs.
    """
    serializer_class = DashboardWithGraphsSerializer
    
    def get_queryset(self):
        """Return optimized queryset for monthly dashboards."""
        return Dashboard.objects.filter(type_dashboard="monthly")
        
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve method to add caching."""
        return super().retrieve(request, *args, **kwargs)
