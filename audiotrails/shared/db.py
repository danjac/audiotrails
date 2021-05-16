from typing import TYPE_CHECKING

from django.db import connections
from django.db.models import QuerySet

if TYPE_CHECKING:
    Base: QuerySet = QuerySet
else:
    Base = object


class FastCountMixin(Base):
    def count(self):
        if self._query.group_by or self._query.where or self._query.distinct:
            return super().count()
        cursor = connections[self.db].cursor()
        cursor.execute(
            "SELECT reltuples FROM pg_class WHERE relname = %s",
            [self.model._meta.db_table],
        )
        n = int(cursor.fetchone()[0])
        if n >= 1000:
            return n  # exact count for small tables
        return super().count()
