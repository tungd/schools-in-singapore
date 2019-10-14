from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from . import models


@registry.register_document
class SchoolDocument(Document):
    class Index:
        name = 'schools'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = models.School
        fields = [f.name for f in models.School._meta.fields[1:]]
        queryset_pagination = 512
