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

        strategy = self.request.query_params\
                               .get('strategy', 'keyword_recognition')
        if strategy == 'boosting':
            # Boosting strategy: i.e ?q=west
            # First result before: id=102, after: id=18
            # fields = models.School.field_names
            fields = [f'{field}^4.0' if field == 'zone_code' else field
                      for field in models.School.field_names]
            match = MultiMatch(query=query, fields=fields)
        else:
            # Keyword recognition strategy: i.e ?q=west
            fields = models.School.field_names
            match = MultiMatch(query=query, fields=fields)

        return documents.SchoolDocument.search().query(match).to_queryset()
