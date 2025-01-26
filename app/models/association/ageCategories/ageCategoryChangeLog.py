"""
Changelog for age categories.

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
from app.models.association.ageCategories.ageCategoryLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.association.ageCategories.ageCategory import AgeCategory


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class AgeCategoryChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association_age_category_changelog'

    # TRACK CHANGES ####################################################################################################
    __trackedFields__ = {'name', 'description', 'key', 'deadlineMin', 'deadlineMax', 'ageMin', 'ageMax'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'object_fk', sqlalchemy.ForeignKey('association_age_category.uid'), index=True, nullable=False)
    new_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_name', sqlalchemy.String(64))
    new_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_description', sqlalchemy.String(4096))
    new_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_key', sqlalchemy.String(32))
    new_deadline_min: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_deadline_min', sqlalchemy.Date)
    new_deadline_max: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_deadline_max', sqlalchemy.Date)
    new_age_min: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_age_min', sqlalchemy.Integer())
    new_age_max: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_age_max', sqlalchemy.Integer())

    old_name: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_name', sqlalchemy.String(64))
    old_description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_description', sqlalchemy.String(4096))
    old_key: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_key', sqlalchemy.String(32))
    old_deadline_min: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_deadline_min', sqlalchemy.Date)
    old_deadline_max: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_deadline_max', sqlalchemy.Date)
    old_age_min: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_age_min', sqlalchemy.Integer())
    old_age_max: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_age_max', sqlalchemy.Integer())

    # RELATIONSHIP #####################################################################################################
    ageCategory: sqlalchemy.orm.Mapped['AgeCategory'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='AgeCategoryChangeLog.objectFK')
