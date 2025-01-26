"""
DB Model for Clubs.

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
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.club.club import ClubChangeLog

# HELPERS ##############################################################################################################
from app.models.club.club.clubLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Club(MutableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'name', 'abbreviation', 'established', 'matricule', 'rbe', 'nace', 'minVotingAge',
                   'fiscalYearStart', 'fiscalYearEnd'}
    __required__ = {'name', 'abbreviation', 'established', 'minVotingAge', 'fiscalYearStart', 'fiscalYearEnd'}
    __mutable__ = {'name', 'abbreviation', 'established', 'matricule', 'rbe', 'nace', 'minVotingAge',
                   'fiscalYearStart', 'fiscalYearEnd'}
    __unique__ = {'name', 'abbreviation', 'matricule', 'rbe', 'nace'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'name', sqlalchemy.String(64), unique=True, nullable=False)
    abbreviation: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'abbreviation', sqlalchemy.String(32), unique=True, nullable=False)
    established: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'established', sqlalchemy.Date, nullable=False)
    minVotingAge: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'min_voting_age', sqlalchemy.Integer(), nullable=False)
    matricule: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'matricule', sqlalchemy.String(32))
    rbe: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'rbe', sqlalchemy.String(32))
    nace: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'nace', sqlalchemy.String(32))
    fiscalYearStart: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'fiscal_year_start', sqlalchemy.Date, nullable=False)
    fiscalYearEnd: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'fiscal_year_end', sqlalchemy.Date, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['ClubChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='club',
        foreign_keys='ClubChangeLog.objectFK',
        order_by='desc(ClubChangeLog.when)')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f'{self.name}'
