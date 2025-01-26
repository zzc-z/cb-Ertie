"""
Changelog for membership types.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.changeLogMixing import ChangeLogMixin
from app.models.club.membershipTypes.membershipTypeLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.club.membershipTypes.membershipType import MembershipType


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MembershipTypeChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_membership_type_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'key', 'name', 'description', 'fee', 'vote'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey(
                                                                            'club_membership_type.uid'),
                                                                        index=True, nullable=False)

    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_key',
                                                                                 sqlalchemy.String(32))
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_description',
                                                                                         sqlalchemy.String(4096))
    new_fee: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('new_fee',
                                                                                   sqlalchemy.Float)
    new_vote: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('new_vote',
                                                                                   sqlalchemy.Boolean)
    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_key',
                                                                                 sqlalchemy.String(32))
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_description',
                                                                                         sqlalchemy.String(4096))
    old_fee: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('old_fee',
                                                                                   sqlalchemy.Float)
    old_vote: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('old_vote',
                                                                                   sqlalchemy.Boolean)

    # RELATIONSHIP #####################################################################################################
    membershipType: sqlalchemy.orm.Mapped['MembershipType'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='MembershipTypeChangeLog.objectFK')
