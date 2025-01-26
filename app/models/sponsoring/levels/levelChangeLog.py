"""
Changelog for sponsoring levels.

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
from app.models.sponsoring.levels.levelLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.sponsoring.levels.level import Level


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class LevelChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsoring_level_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'key', 'name', 'description', 'threshold', 'limit'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('sponsoring_level.uid'),
                                                                        index=True, nullable=False)
    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_key',
                                                                                 sqlalchemy.String(32))
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_description',
                                                                                         sqlalchemy.String(4096))
    new_threshold: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('new_threshold',
                                                                                         sqlalchemy.Float)

    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_key',
                                                                                 sqlalchemy.String(32))
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_description',
                                                                                         sqlalchemy.String(4096))
    old_threshold: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('old_threshold',
                                                                                         sqlalchemy.Float)

    # RELATIONSHIP #####################################################################################################
    level: sqlalchemy.orm.Mapped['Level'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='LevelChangeLog.objectFK')
