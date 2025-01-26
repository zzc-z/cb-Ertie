"""
DB Model for Board Types.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.members.membersBoardElection import MemberBoardElection
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.club.boardTypes.boardTypeLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.club.boardTypes import BoardTypeChangeLog


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class BoardType(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_board_type'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['name', 'key', 'description']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'name', 'description', 'key', 'term'}
    __required__ = {'name', 'description', 'key', 'term'}
    __mutable__ = {'name', 'description', 'key', 'term'}
    __unique__ = {'name', 'key', 'description'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096),
                                                                           unique=True, nullable=False)
    term: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('term', sqlalchemy.Integer,
                                                                    nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['BoardTypeChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='boardType',
        foreign_keys='BoardTypeChangeLog.objectFK',
        order_by='desc(BoardTypeChangeLog.when)')

    boardElections: sqlalchemy.orm.Mapped[Optional[List['MemberBoardElection']]] = sqlalchemy.orm.relationship(
        back_populates='position',
        foreign_keys='MemberBoardElection.boardTypeFK')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        # do not delete a board type while there are active members associated with it
        return len(self.boardElections) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
