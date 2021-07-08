from __future__ import annotations

import functools
import operator

from typing import TYPE_CHECKING, ClassVar

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db import connections
from django.db.models import F, Q, QuerySet
from django.utils.encoding import force_str

if TYPE_CHECKING:
    Base: QuerySet = QuerySet  # pragma: no cover
else:
    Base = object


class FastCountMixin(Base):
    def count(self) -> int:
        if self._query.group_by or self._query.where or self._query.distinct:
            return super().count()
        if (count := get_reltuple_count(self.db, self.model._meta.db_table)) >= 1000:
            return count
        # exact count for small tables
        return super().count()


class SearchMixin(Base):
    search_vectors: ClassVar[list[tuple[str, str]]] = []
    search_vector_field: ClassVar[str] = "search_vector"
    search_rank: ClassVar[str] = "rank"

    def search(self, search_term: str) -> QuerySet:
        if not search_term:
            return self.none()

        query = SearchQuery(force_str(search_term), search_type="websearch")
        ranks: dict[str, SearchRank | list[F]] = {}
        filters: list[Q] = []

        if self.search_vectors:

            combined_rank: list[F] = []

            for field, rank in self.search_vectors:
                ranks[rank] = SearchRank(F(field), query=query)
                combined_rank.append(F(rank))
                filters.append(Q(**{field: query}))

            ranks[self.search_rank] = functools.reduce(operator.add, combined_rank)

        else:
            ranks[self.search_rank] = SearchRank(
                F(self.search_vector_field), query=query
            )
            filters.append(Q(**{self.search_vector_field: query}))

        return self.annotate(**ranks).filter(functools.reduce(operator.or_, filters))


def get_reltuple_count(db: str, table: str) -> int:
    cursor = connections[db].cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s", [table])
    return int(cursor.fetchone()[0])
