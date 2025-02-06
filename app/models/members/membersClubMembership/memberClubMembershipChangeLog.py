"""
DB Changelog Model for Club Memberships

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.changeLogMixing import ChangeLogMixin

# TYPE HINTS ###########################################################################################################
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.membersClubMembership import MemberClubMembership

# HELPERS ##############################################################################################################
from app.models.members.membersClubMembership.memberClubMembershipLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberClubMembershipChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_club_membership_changelog'

    # TRACKED FIELDS ###################################################################################################
    __trackedFields__ = {'membershipTypeFK', 'birthday', 'joined', 'left', 'active', 'coach',
                         'lastPayment', 'clothingSize', 'nationality'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'object_fk', sqlalchemy.ForeignKey('member_club_membership.uid'), index=True, nullable=False)

    new_membershipTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_membership_type_fk', sqlalchemy.Integer)
    new_birthday: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_birthday', sqlalchemy.Date)
    new_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_joined', sqlalchemy.Date)
    new_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_left', sqlalchemy.Date)
    new_active: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('new_active')
    new_lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_last_payment', sqlalchemy.Date)
    new_clothingSize: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_clothing_size', sqlalchemy.String(8))
    new_nationality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_nationality',
                                                                                         sqlalchemy.String(3))
    new_coach: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('new_coach',
                                                                                    sqlalchemy.Boolean)

    old_membershipTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_membership_type_fk', sqlalchemy.Integer)
    old_birthday: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_birthday', sqlalchemy.Date)
    old_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_joined', sqlalchemy.Date)
    old_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_left', sqlalchemy.Date)
    old_active: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column(
        'old_active')
    old_lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_last_payment', sqlalchemy.Date)
    old_clothingSize: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_clothing_size', sqlalchemy.String(8))
    old_nationality: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_nationality', sqlalchemy.String(3))
    old_coach: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('old_coach',
                                                                                    sqlalchemy.Boolean)

    # RELATIONSHIPS ####################################################################################################
    memberClubMembership: sqlalchemy.orm.Mapped['MemberClubMembership'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='MemberClubMembershipChangeLog.objectFK')
