from rest_framework import generics

from .models import Menu
from .serializers import MenuSerializer


class MenuCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        if category_id:
            return Menu.objects.filter(category_id=category_id)
        return Menu.objects.all()

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
