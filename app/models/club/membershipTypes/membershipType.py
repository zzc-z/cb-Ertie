"""
DB Model for Membership Types

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.club.membershipTypes.membershipTypeLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.club.membershipTypes.membershipTypeChangeLog import MembershipTypeChangeLog
    from app.models.members.membersClubMembership import MemberClubMembership


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MembershipType(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_membership_type'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description', 'fee']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'description', 'fee', 'vote'}
    __required__ = {'key', 'name', 'description', 'fee', 'vote'}
    __mutable__ = {'key', 'name', 'description', 'fee', 'vote'}
    __unique__ = {'key', 'name', 'description'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096), unique=True)
    fee: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column('fee', sqlalchemy.Float)
    vote: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column('vote', sqlalchemy.Boolean)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['MembershipTypeChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='membershipType',
        foreign_keys='MembershipTypeChangeLog.objectFK',
        order_by='desc(MembershipTypeChangeLog.when)')

    clubMemberships: sqlalchemy.orm.Mapped[Optional[List['MemberClubMembership']]] = sqlalchemy.orm.relationship(
        back_populates='membershipType', foreign_keys='MemberClubMembership.membershipTypeFK')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        # do not delete a membership type while active members are associated with it
        return len(self.clubMemberships) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
