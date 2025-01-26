"""
Changelog for clubs.

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
    from app.models.club.club import Club

# HELPERS ##############################################################################################################
from app.models.club.club.clubLuxNames import luxNames


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class ClubChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'name', 'abbreviation', 'established', 'matricule', 'rbe', 'nace', 'minVotingAge',
                         'fiscalYearStart', 'fiscalYearEnd'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('club.uid'),
                                                                        index=True, nullable=False)
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_name', sqlalchemy.String(64))
    new_abbreviation: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_abbreviation', sqlalchemy.String(32))
    new_established: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_established', sqlalchemy.Date)
    new_matricule: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_matricule', sqlalchemy.String(32))
    new_rbe: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_rbe', sqlalchemy.String(32))
    new_nace: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_nace', sqlalchemy.String(32))
    new_minVotingAge: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_min_voting_age', sqlalchemy.Integer)
    new_fiscalYearStart: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_fiscal_year_start', sqlalchemy.Date)
    new_fiscalYearEnd: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_fiscal_year_end', sqlalchemy.Date)

    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_name', sqlalchemy.String(64))
    old_abbreviation: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_abbreviation', sqlalchemy.String(32))
    old_established: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_established', sqlalchemy.Date)
    old_minVotingAge: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_min_voting_age', sqlalchemy.Integer)
    old_matricule: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_matricule', sqlalchemy.String(32))
    old_rbe: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_rbe', sqlalchemy.String(32))
    old_nace: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_nace', sqlalchemy.String(32))
    old_fiscalYearStart: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_fiscal_year_start', sqlalchemy.Date)
    old_fiscalYearEnd: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_fiscal_year_end', sqlalchemy.Date)

    # RELATIONSHIP #####################################################################################################
    club: sqlalchemy.orm.Mapped['Club'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='ClubChangeLog.objectFK')
