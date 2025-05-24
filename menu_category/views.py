from rest_framework import generics

from .models import MenuCategory
from .serializers import MenuCategorySerializer


class MenuCategoryCreateView(generics.ListCreateAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = MenuCategory.objects.all()
        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add any additional context if needed
        return context


class MenuCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add any additional context if needed
        return context
