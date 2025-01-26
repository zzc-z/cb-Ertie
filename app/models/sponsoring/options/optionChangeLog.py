"""
Changelog for sponsoring options.

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
from app.models.sponsoring.options.optionLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.sponsoring.options.option import Option


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class OptionChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsoring_option_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'key', 'name', 'description', 'value', 'term', 'limit'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('sponsoring_option.uid'),
                                                                        index=True, nullable=False)
    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_key',
                                                                                 sqlalchemy.String(32))
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_name',
                                                                                  sqlalchemy.String(64))
    new_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_description',
                                                                                         sqlalchemy.String(4096))
    new_value: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('new_value',
                                                                                     sqlalchemy.Float)
    new_term: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('new_term',
                                                                                  sqlalchemy.Integer)
    new_limit: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('new_limit',
                                                                                   sqlalchemy.Integer)

    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_key',
                                                                                 sqlalchemy.String(32))
    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_name',
                                                                                  sqlalchemy.String(64))
    old_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_description',
                                                                                         sqlalchemy.String(4096))
    old_value: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column('old_value',
                                                                                     sqlalchemy.Float)
    old_term: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('old_term',
                                                                                  sqlalchemy.Integer)
    old_limit: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('old_limit',
                                                                                   sqlalchemy.Integer)

    # RELATIONSHIP #####################################################################################################
    option: sqlalchemy.orm.Mapped['Option'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='OptionChangeLog.objectFK')
