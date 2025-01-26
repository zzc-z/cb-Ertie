"""
DB Model for Assocations.

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
from app.models.mutableMixin import MutableMixin

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.association.association import AssociationChangeLog

# HELPERS ##############################################################################################################
from app.models.association.association.associationNamesLux import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Association(MutableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'name', 'abbreviation', 'fee', 'seasonStart', 'seasonEnd'}
    __required__ = {'name', 'abbreviation', 'fee', 'seasonStart', 'seasonEnd'}
    __mutable__ = {'name', 'abbreviation', 'fee', 'seasonStart', 'seasonEnd'}
    __unique__ = {'name', 'abbreviation'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'name', sqlalchemy.String(64), unique=True, nullable=False)
    abbreviation: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'abbreviation', sqlalchemy.String(32), unique=True, nullable=False)
    fee: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column(
        'fee', sqlalchemy.Float, nullable=False)
    seasonStart: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'season_start', sqlalchemy.Date, nullable=False)
    seasonEnd: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'season_end', sqlalchemy.Date, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['AssociationChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='association',
        foreign_keys='AssociationChangeLog.objectFK',
        order_by='desc(AssociationChangeLog.when)')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f'{self.name}'
