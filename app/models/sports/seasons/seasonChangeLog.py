"""
Changelog for seasons.

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
from app.models.sports.seasons.seasonLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.sports.seasons.season import Season


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class SeasonChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sports_season_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'key', 'name', 'completed', 'begin', 'end'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('sports_season.uid'),
                                                                        index=True, nullable=False)
    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_key',
                                                                                 sqlalchemy.String(32))
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_completed: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('new_completed',
                                                                                        sqlalchemy.Boolean)
    new_start: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_start',
                                                                                    sqlalchemy.Date)
    new_end: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_end',
                                                                                    sqlalchemy.Date)
    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_key',
                                                                                 sqlalchemy.String(32))
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_completed: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column('old_completed',
                                                                                        sqlalchemy.Boolean)
    old_start: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_start',
                                                                                    sqlalchemy.Date)
    old_end: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_end',
                                                                                    sqlalchemy.Date)

    # RELATIONSHIP #####################################################################################################
    season: sqlalchemy.orm.Mapped['Season'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='SeasonChangeLog.objectFK')
