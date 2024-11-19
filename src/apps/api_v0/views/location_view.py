from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.accounting.models import Location
from apps.api_v0.serializers.location import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)