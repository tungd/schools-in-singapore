from django_elasticsearch_dsl import DocType, Index

from . import models

schools = Index('schools')

schools.settings(
    number_of_shards=4,
    number_of_replicas=0
)


@schools.doc_type
class SchoolDocument(DocType):
    class Meta:
        model = models.School
        fields = models.School.field_names
        queryset_pagination = 512
