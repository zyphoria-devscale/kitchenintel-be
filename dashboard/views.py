from datetime import timedelta, datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dashboard
from .serializers import DashboardWithGraphsSerializer
from shared.utils import parse_date_string
from .task import custom_task


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


class GeneratePastData(APIView):
    def post(self, request, *args, **kwargs):
        # Access query parameters from the URL
        from_date = request.query_params.get('from_date','2025-05-01')
        to_date = request.query_params.get('to_data', '2025-05-31')
        type_report = request.query_params.get('type_report', 'daily')

        start_date = parse_date_string(from_date)
        end_date = parse_date_string(to_date)

        if start_date > end_date:
            return Response({
                'message': 'Invalid date range'
            }, status=status.HTTP_400_BAD_REQUEST)

        if type_report not in ['daily','weekly','monthly']:
            return Response({
                'message': 'Invalid report type'
            })

        if type_report == 'daily':
            while start_date <= end_date:
                custom_task(start_date,start_date,type_report)
                start_date += timedelta(days=1)

        if type_report == 'weekly':
            while start_date <= end_date:
                week_start = start_date - timedelta(days=start_date.weekday())
                week_end = week_start + timedelta(days=6)
                custom_task(week_start,week_end,type_report)
                start_date = week_end + timedelta(days=1)

        if type_report == 'monthly':
            while start_date <= end_date:
                month_start = start_date.replace(day=1)
                month_end = datetime(year=month_start.year, month=month_start.month+1, day=1).date() - timedelta(days=1)
                custom_task(month_start,month_end,type_report)
                start_date = month_end + timedelta(days=1)



        return Response({
            'message': 'Ok!'
        }, status=status.HTTP_201_CREATED)
