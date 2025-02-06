"""
DB Model for Board Elections

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
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
from app.models.members import boardElectionPositionsMapping

# HELPERS ##############################################################################################################
from app.models.members.membersBoardElection.memberBoardElectionLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Set, Dict, Optional, TYPE_CHECKING

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
    __columns__ = {'memberFK', 'joined', 'left', 'lastElected'}
    __required__ = {'memberFK', 'joined', 'lastElected'}
    __mutable__ = {'left', 'lastElected'}
    __unique__ = {'memberFK'}
    __uniqueTuples__ = {}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk', sqlalchemy.Integer,
                                                                        sqlalchemy.ForeignKey('member.uid'),
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

    positions: sqlalchemy.orm.Mapped[Set['BoardType']] = sqlalchemy.orm.relationship(
        secondary=boardElectionPositionsMapping,
        back_populates='boardElections',
        order_by='BoardType.name')

    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='boardElection')

    # METHODS ##########################################################################################################
    def viewPayload(self):
        try:
            payload = super().viewPayload()

            # is the election still valid=
            lastElected = next(item for item in payload if item['key'] == 'lastElected')
            lastElected['valid'] = self.electionStillValid(lastElected)
            payload[payload.index(lastElected)] = lastElected

            payload.append({'key': 'positions', 'value': self.positions, 'lux': 'Positiounen', 'position': 1})
            return payload
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection: {e}') from e

    def electionStillValid(self, lastElected:dict) -> bool:
        leDate = lastElected.get('value')

        # get shortest term
        shortestTerm = min((position.term for position in self.positions), default=0)

        if date(leDate.year, leDate.month, leDate.day) < date.today() - timedelta(365 * shortestTerm):
            return False
        else:
            return True

    def addPosition(self, position: 'BoardType') -> None:
        try:
            if position not in self.positions:
                self.positions.add(position)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection.addPosition: {e}')

    def removePosition(self, position: 'BoardType') -> None:
        try:
            if position in self.positions:
                self.positions.remove(position)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection.removePosition: {e}')

    def canBeDeleted(self) -> bool:
        try:
            return False if not self.left else True
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberBoardElection: {e}') from e
