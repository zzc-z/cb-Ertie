"""
DB Model for Board Elections

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# FLASK & PYTHON #######################################################################################################
from datetime import date, timedelta

# DB & MODELS ##########################################################################################################
from flask_login import UserMixin
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.members.membersBoardElection.memberBoardElectionChangeLog import MemberBoardElectionChangeLog

# HELPERS ##############################################################################################################
from app.models.members.membersBoardElection.memberBoardElectionLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.members import Member
    from app.models.club.boardTypes import BoardType


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberBoardElection(MutableMixin, UserMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_board_election'

    # MUTABLE ##########################################################################################################
    __columns__ = {'memberFK', 'boardTypeFK', 'joined', 'left', 'lastElected'}
    __required__ = {'memberFK', 'boardTypeFK', 'joined', 'lastElected'}
    __mutable__ = {'boardTypeFK', 'left', 'lastElected'}
    __unique__ = {'memberFK'}
    __uniqueTuples__ = {}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk', sqlalchemy.Integer,
                                                                        sqlalchemy.ForeignKey('member.uid'),
                                                                        nullable=False)
    boardTypeFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('board_type_fk',
                                                                           sqlalchemy.Integer,
                                                                           sqlalchemy.ForeignKey(
                                                                               'club_board_type.uid'),
                                                                           nullable=False)
    joined: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('joined',
                                                                       sqlalchemy.Date)
    left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('left', sqlalchemy.Date)
    lastElected: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('last_elected',
                                                                            sqlalchemy.Date)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List[MemberBoardElectionChangeLog]] = sqlalchemy.orm.relationship(
        back_populates='memberBoardElection',
        foreign_keys='MemberBoardElectionChangeLog.objectFK', order_by='desc(MemberBoardElectionChangeLog.when)')

    position: sqlalchemy.orm.Mapped['BoardType'] = sqlalchemy.orm.relationship(back_populates='boardElections')
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='boardElection')

    # METHODS ##########################################################################################################
    def viewPayload(self):
        try:
            payload = super().viewPayload()

            # check term
            lastElected = next(item for item in payload if item['key'] == 'lastElected')
            leDate = lastElected.get('value')
            if date(leDate.year, leDate.month, leDate.day) < date.today() - timedelta(365 * self.position.term):
                lastElected['valid'] = False
            else:
                lastElected['valid'] = True
            payload[payload.index(lastElected)] = lastElected
            return payload
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection: {e}') from e

    def canBeDeleted(self) -> bool:
        try:
            return False if not self.left else True
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection: {e}') from e
