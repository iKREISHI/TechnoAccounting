from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.api_v0.serializers.auditorium import AuditoriumSerializer
from apps.university.models import Auditorium


class AuditoriumViewSet(viewsets.ModelViewSet):
    serializer_class = AuditoriumSerializer
    queryset = Auditorium.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)