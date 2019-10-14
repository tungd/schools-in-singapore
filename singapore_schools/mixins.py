from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class ElasticSearchPaginationMixin(object):

    def to_queryset(self, search):
        if isinstance(self.paginator, PageNumberPagination):
            return self._to_queryset_by_page_number(search)

        if isinstance(self.paginator, LimitOffsetPagination):
            return self._to_queryset_by_limit_offset(search)

        raise NotImplementedError(
            '{} is not supported'.format(self.paginator.__class__)
        )

    def _to_queryset_by_page_number(self, search):
        self.paginator.request = self.request
        page_size = self.paginator.get_page_size(self.request)
        if not page_size:
            return None

        paginator = self.paginator.django_paginator_class(search, page_size)
        page_number = self.request.query_params.get(self.paginator.page_query_param, 1)
        if page_number in self.paginator.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.paginator.page = paginator.page(page_number)
        except InvalidPage as e:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(e)
            )
            raise NotFound(msg)

        return self.paginator.page.object_list.to_queryset()

    def _to_queryset_by_limit_offset(self, search):
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
