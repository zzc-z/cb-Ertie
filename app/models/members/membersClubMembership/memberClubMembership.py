"""
DB Model for Member ClubMembership

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# FLASK & PYTHON #######################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
from flask_login import UserMixin
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.members.membersClubMembership.memberClubMembershipChangeLog import MemberClubMembershipChangeLog
from app.models.club.club import Club

# HELPERS ##############################################################################################################
from app.models.members.membersClubMembership.memberClubMembershipLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.members import Member
    from app.models.club.membershipTypes import MembershipType


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberClubMembership(MutableMixin, UserMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_club_membership'

    # MUTABLE ##########################################################################################################
    __columns__ = {'memberFK', 'membershipTypeFK', 'birthday', 'joined', 'left',
                   'active', 'lastPayment', 'clothingSize', 'nationality', 'coach'}
    __required__ = {'memberFK', 'membershipTypeFK', 'nationality', 'clothingSize', 'active'}
    __mutable__ = {'membershipTypeFK', 'birthday', 'joined', 'left', 'coach',
                   'active', 'lastPayment', 'clothingSize', 'nationality'}
    __unique__ = {'memberFK'}
    __uniqueTuples__ = {}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk', sqlalchemy.Integer,
                                                                        sqlalchemy.ForeignKey('member.uid'),
                                                                        nullable=False)
    membershipTypeFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('membership_type_fk',
                                                                                sqlalchemy.Integer,
                                                                                sqlalchemy.ForeignKey(
                                                                                    'club_membership_type.uid'),
                                                                                nullable=False)
    birthday: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('birthday',
                                                                                   sqlalchemy.Date)
    joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('joined',
                                                                                 sqlalchemy.Date)
    left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('left', sqlalchemy.Date)
    active: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column('active', nullable=False)
    lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('last_payment',
                                                                                      sqlalchemy.Date)
    clothingSize: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('clothing_size',
                                                                                      sqlalchemy.String(8),
                                                                                      nullable=False)
    nationality: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('nationality',
                                                                           sqlalchemy.String(3),
                                                                           nullable=False)
    coach: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column('coach',
                                                                      sqlalchemy.Boolean, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List[MemberClubMembershipChangeLog]] = sqlalchemy.orm.relationship(
        back_populates='memberClubMembership',
        foreign_keys='MemberClubMembershipChangeLog.objectFK', order_by='desc(MemberClubMembershipChangeLog.when)')

    membershipType: sqlalchemy.orm.Mapped['MembershipType'] = sqlalchemy.orm.relationship(
        back_populates='clubMemberships')
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='clubMembership')

    # METHODS ##########################################################################################################
    def viewPayload(self, sort: bool = True):
        try:
            payload = super().viewPayload()

            # check last payment date
            lastPayment = next((item for item in payload if item['key'] == 'lastPayment'), None)
            if lastPayment is None:
                payload.append({
                    'lux': 'Memberskaart',
                    'key': 'lastPayment',
                    'value': None
                })
            else:
                lpDate = lastPayment.get('value')

                # get the end date of the club's fiscal year
                club = database.getObjects(Club)[0]
                fiscalYearEnd = club.fiscalYearEnd

                # calculate the year of the next fiscal end date ; add 1 to the year if the end year has already passed
                today = date.today()
                nextFiscalYearEnd = date(
                    today.year + (1 if date(today.year, fiscalYearEnd.month, fiscalYearEnd.day) < today else 0),
                    fiscalYearEnd.month,
                    fiscalYearEnd.day)

                # now check whether the last payment was done before the fiscal year-end date
                lastPayment['valid'] = lpDate < nextFiscalYearEnd
                payload[payload.index(lastPayment)] = lastPayment

            return payload
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberClubMembership: {e}') from e

    def canBeDeleted(self) -> bool:
        try:
            return not self.active
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberClubMembership: {e}') from e
