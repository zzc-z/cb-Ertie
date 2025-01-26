"""
DB Model for Age Categories.

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
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.association.ageCategories.ageCategoryLuxNames import luxNames
from app.models.association.competitions import Competition
from app.models.club.practiceTypes.practiceType import PracticeType
from app.models.association import competitionAgeCategoriesMapping
from app.models.club import practiceTypeAgeCategoriesMapping

# TYPE HINTS ###########################################################################################################
from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.association.ageCategories.ageCategoryChangeLog import AgeCategoryChangeLog
    from app.models.members.members import Member


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class AgeCategory(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association_age_category'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['name', 'key', 'description']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'name', 'description', 'key', 'deadlineMin', 'deadlineMax', 'ageMin', 'ageMax'}
    __required__ = {'name', 'description', 'key', 'deadlineMin', 'deadlineMax', 'ageMin', 'ageMax'}
    __mutable__ = {'name', 'description', 'key', 'deadlineMin', 'deadlineMax', 'ageMin', 'ageMax'}
    __unique__ = {'name', 'description', 'key'}
    __uniqueTuples__ = [('ageMin', 'ageMax')]
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'name', sqlalchemy.String(64), unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'description', sqlalchemy.String(4096), unique=True, nullable=False)
    deadlineMin: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'deadline_min', sqlalchemy.Date, nullable=False)
    deadlineMax: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column(
        'deadline_max', sqlalchemy.Date, nullable=False)
    ageMin: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'age_min', sqlalchemy.Integer(), nullable=False)
    ageMax: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'age_max', sqlalchemy.Integer(), nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['AgeCategoryChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='ageCategory',
        foreign_keys='AgeCategoryChangeLog.objectFK',
        order_by='desc(AgeCategoryChangeLog.when)')

    competitions: sqlalchemy.orm.Mapped[Set['Competition']] = sqlalchemy.orm.relationship(
        secondary=competitionAgeCategoriesMapping,
        back_populates='ageCategories')

    practiceTypes: sqlalchemy.orm.Mapped[Set['PracticeType']] = sqlalchemy.orm.relationship(
        secondary=practiceTypeAgeCategoriesMapping,
        back_populates='ageCategories')

    # METHODS ##########################################################################################################
    def eligibleMembers(self, members: List['Member'], leqMin: bool = False, leqMax: bool = False) -> List['Member']:
        try:
            return [member for member in members if member.eligibleForAgeCategory(self, leqMin=leqMin, leqMax=leqMax)]

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ AgeCategory.getEligibleMembers: {e}')

    def canBeDeleted(self) -> bool:
        return len(self.competitions) == 0 and len(self.practiceTypes) == 0

    # OVERRIDES ########################################################################################################
    def __repr__(self) -> str:
        return f'{self.name}'
