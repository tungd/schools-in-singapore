from elasticsearch_dsl.query import MultiMatch
from rest_framework.generics import ListAPIView

from . import documents, models, serializers


class SchoolListView(ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is None:
            return self.queryset

        match = MultiMatch(query=query, fields=models.School.field_names)
        return documents.SchoolDocument.search().query(match).to_queryset()
