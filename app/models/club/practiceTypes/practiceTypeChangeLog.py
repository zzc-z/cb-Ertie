"""
Changelog for practice types.

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
from app.models.club.practiceTypes.practiceTypeLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.club.practiceTypes.practiceType import PracticeType


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class PracticeTypeChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_practice_type_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'key', 'name', 'gender', 'description'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey(
                                                                            'club_practice_type.uid'),
                                                                        index=True, nullable=False)
    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_key',
                                                                                 sqlalchemy.String(32))
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_description',
                                                                                         sqlalchemy.String(4096))
    new_gender: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_gender',
                                                                                    sqlalchemy.String(1))

    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_key',
                                                                                 sqlalchemy.String(32))
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_description',
                                                                                         sqlalchemy.String(4096))
    old_gender: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_gender',
                                                                                    sqlalchemy.String(1))

    # RELATIONSHIP #####################################################################################################
    practiceType: sqlalchemy.orm.Mapped['PracticeType'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='PracticeTypeChangeLog.objectFK')
