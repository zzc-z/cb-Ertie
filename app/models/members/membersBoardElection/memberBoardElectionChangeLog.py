"""
DB Changelog Model for Club Board Elections

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
    from app.models.members.membersBoardElection import MemberBoardElection

# HELPERS ##############################################################################################################
from app.models.members.membersBoardElection.memberBoardElectionLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberBoardElectionChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_board_election_changelog'

    # TRACKED FIELDS ###################################################################################################
    __trackedFields__ = {'boardTypeFK', 'joined', 'left', 'lastElected'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'object_fk', sqlalchemy.ForeignKey('member_board_election.uid'), index=True, nullable=False)

    new_boardTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_board_type_fk', sqlalchemy.Integer)
    new_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_joined', sqlalchemy.Date)
    new_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_left', sqlalchemy.Date)
    new_lastElected: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_last_elected', sqlalchemy.Date)

    old_boardTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_board_type_fk', sqlalchemy.Integer)
    old_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_joined', sqlalchemy.Date)
    old_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_left', sqlalchemy.Date)
    old_lastElected: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_last_elected', sqlalchemy.Date)

    # RELATIONSHIPS ####################################################################################################
    memberBoardElection: sqlalchemy.orm.Mapped['MemberBoardElection'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='MemberBoardElectionChangeLog.objectFK')
