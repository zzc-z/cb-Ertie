"""
Changelog for practices.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# PYTHON ###############################################################################################################
from datetime import date, time

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.changeLogMixing import ChangeLogMixin
from app.models.sports.practiceSessions.practiceSessionLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.sports.practiceSessions.practiceSession import PracticeSession


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class PracticeSessionChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sports_practice_session_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'date', 'remark', 'start', 'end', 'practiceTypeFK', 'seasonFK'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'object_fk', sqlalchemy.ForeignKey('sports_practice_session.uid'), index=True, nullable=False)

    new_remark: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_remark',
                                                                                    sqlalchemy.String(4096))
    new_date: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_date',
                                                                                   sqlalchemy.Date)
    new_start: sqlalchemy.orm.Mapped[Optional[time]] = sqlalchemy.orm.mapped_column('new_start',
                                                                                    sqlalchemy.Time)
    new_end: sqlalchemy.orm.Mapped[Optional[time]] = sqlalchemy.orm.mapped_column('new_end', sqlalchemy.Time)
    new_practiceTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_practice_type_fk', sqlalchemy.Integer)

    old_remark: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_remark',
                                                                                    sqlalchemy.String(4096))
    old_date: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_date',
                                                                                   sqlalchemy.Date)
    old_start: sqlalchemy.orm.Mapped[Optional[time]] = sqlalchemy.orm.mapped_column('old_start',
                                                                                    sqlalchemy.Time)
    old_end: sqlalchemy.orm.Mapped[Optional[time]] = sqlalchemy.orm.mapped_column('old_end', sqlalchemy.Time)
    old_practiceTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_practice_type_fk', sqlalchemy.Integer)

    # RELATIONSHIP #####################################################################################################
    practiceSession: sqlalchemy.orm.Mapped['PracticeSession'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='PracticeSessionChangeLog.objectFK')
