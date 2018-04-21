from rest_framework.generics import ListAPIView

from . import models, serializers


class SchoolListView(ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
