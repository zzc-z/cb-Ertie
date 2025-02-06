"""
This class serves as glue between the actual DB and the fulltext search engine.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy
from app.factory.extensions import database
from app.factory.extensions.custom.fullTextSearch import fullTextSearch

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import flask_sqlalchemy


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class SearchableMixin:
    @classmethod
    def search(cls, expression: str, returnList: bool = False) -> tuple[list[sqlalchemy.engine.ScalarResult], int]:
        try:
            # noinspection PyUnresolvedReferences
            ids, total = fullTextSearch.queryIndex(index=cls.__tablename__,
                                                   query=expression, resync=False)
            if total == 0:
                return [], 0

            when = []
            for i in range(len(ids)):
                when.append((ids[i], i))

            # noinspection PyUnresolvedReferences
            query = sqlalchemy.select(cls).where(cls.uid.in_(ids)).order_by(database.db.case(*when, value=cls.uid))
            if not returnList:
                return database.db.session.scalars(query), total
            else:
                return database.db.session.scalars(query).all(), total
        except Exception as e:
            raise RuntimeError(f'Runtime Error (SearchableMixin.search): {e}') from e

    @classmethod
    def beforeCommit(cls, session: 'flask_sqlalchemy.session') -> None:
        try:
            session._changes = {
                'add': [obj for obj in session.new if isinstance(obj, cls)],
                'update': [obj for obj in session.dirty if isinstance(obj, cls)],
                'delete': [obj for obj in session.deleted if isinstance(obj, cls)]}
        except Exception as e:
            raise RuntimeError(f'Runtime Error (SearchableMixin.beforeCommit): {e}') from e

    @classmethod
    def afterCommit(cls, session: 'flask_sqlalchemy.session') -> None:
        try:
            for obj in session._changes['add']:
                fullTextSearch.addToIndex(obj.__tablename__, obj)
            for obj in session._changes['update']:
                fullTextSearch.addToIndex(obj.__tablename__, obj)
            for obj in session._changes['delete']:
                fullTextSearch.removeFromIndex(obj.__tablename__, obj)
            session._changes = None
        except Exception as e:
            raise RuntimeError(f'Runtime Error (SearchableMixin.afterCommit): {e}') from e

    @classmethod
    def reindex(cls) -> None:
        try:
            for obj in database.db.session.scalars(sqlalchemy.select(cls)):
                # noinspection PyUnresolvedReferences
                fullTextSearch.addToIndex(cls.__tablename__, obj)
        except Exception as e:
            raise RuntimeError(f'Runtime Error (SearchableMixin.reindex): {e}') from e


# LISTENERS ############################################################################################################
database.db.event.listen(database.db.session, 'before_commit', SearchableMixin.beforeCommit)
database.db.event.listen(database.db.session, 'after_commit', SearchableMixin.afterCommit)
