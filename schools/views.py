import logging

from django.core.cache import caches
from elasticsearch_dsl.query import MultiMatch
from rest_framework.generics import ListAPIView

from . import documents, models, serializers

field_keywords_cache = caches['field_keywords']


class ElasticSearchPaginationMixin(object):

    def to_queryset(self, search):
        # https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py#L372
        self.paginator.request = self.request

        self.paginator.limit = self.paginator.get_limit(self.request)
        if self.paginator.limit is None:
            return search.to_queryset()

        self.paginator.count = search.count()
        self.paginator.offset = self.paginator.get_offset(self.request)
        if self.paginator.count == 0 or self.paginator.offset > self.paginator.count:
            return []

        return search[
            self.paginator.offset:self.paginator.offset + self.paginator.limit
        ].to_queryset()

    def paginate_queryset(self, queryset):
        # The queryset has already been paginated
        return list(queryset)


class SchoolListView(ElasticSearchPaginationMixin, ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer

    keyword_fields = [
        'zone_code', 'cluster_code',
        'session', 'type', 'main_level', 'language'
    ]

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is None:
            return self.queryset

        search = documents.SchoolDocument.search()
        words = query.split(',')

        strategy = self.request.query_params\
                               .get('strategy', 'keyword_recognition')
        if strategy == 'boosting':
            # Boosting strategy: i.e ?q=goverment+school
            # First result before: id=102, after: id=18
            # fields = models.School.field_names
            fields = [f'{field}^4.0' if field == 'zone_code' else field
                      for field in documents.SchoolDocument.Django.fields]
            match = MultiMatch(query=' '.join(words), fields=fields)
            search = search.query(match)

        else:
            # Keyword recognition strategy: i.e ?q=west
            filters = {}
            for word in words:
                for field_name in self.keyword_fields:
                    if word.lower() in self._values_of(field_name):
                        # Simplified example, doesn't handle multiple keywords
                        # on one field. Probably need defaultdict(list) with
                        # 'or' queries
                        filters[field_name] = word

            # Only perform search on remaining fields
            fields = list(documents.SchoolDocument.Django.fields - filters.keys())
            logging.debug([words, fields, filters])

            match = MultiMatch(query=' '.join(words), fields=fields)
            search = search.query(match)

            # Apply the filters
            for field_name, value in filters.items():
                search = search.filter('term', **{field_name: value})

        return self.to_queryset(search)

    def _values_of(self, field_name):
        values = field_keywords_cache.get(field_name, None)
        if values is None:
            values = [v[field_name].lower()
                      for v in models.School.objects.values(field_name).distinct()]
            field_keywords_cache.set(field_name, values)
        return values
