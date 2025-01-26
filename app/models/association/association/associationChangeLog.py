"""
Changelog for Associations.

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
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.association.association import Association

# HELPERS ##############################################################################################################
from app.models.association.association.associationNamesLux import luxNames


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class AssociationChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'name', 'abbreviation', 'fee', 'seasonStart', 'seasonEnd'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('association.uid'),
                                                                        index=True, nullable=False)
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_name', sqlalchemy.String(64))
    new_abbreviation: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_abbreviation', sqlalchemy.String(32))
    new_fee: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column(
        'new_fee', sqlalchemy.Float)
    new_seasonStart: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_season_start', sqlalchemy.Date)
    new_seasonEnd: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_season_end', sqlalchemy.Date)

    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_name', sqlalchemy.String(64))
    old_abbreviation: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_abbreviation', sqlalchemy.String(32))
    old_fee: sqlalchemy.orm.Mapped[Optional[float]] = sqlalchemy.orm.mapped_column(
        'old_fee', sqlalchemy.Float)
    old_seasonStart: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_season_start', sqlalchemy.Date)
    old_seasonEnd: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_season_end', sqlalchemy.Date)

    # RELATIONSHIP #####################################################################################################
    association: sqlalchemy.orm.Mapped['Association'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='AssociationChangeLog.objectFK')
