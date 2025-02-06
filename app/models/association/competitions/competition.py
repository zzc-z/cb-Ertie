"""
DB Model for Competition Types.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin
from app.models.association.competitions.competitionLuxNames import luxNames
from app.models.association import competitionAgeCategoriesMapping

# TYPE HINTS ###########################################################################################################
from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.association.competitions.competitionChangeLog import CompetitionChangeLog
    from app.models.association.ageCategories.ageCategory import AgeCategory
    from app.models.members.members import Member


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Competition(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association_competition'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['name', 'key', 'description']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'name', 'description', 'key', 'gender'}
    __required__ = {'name', 'description', 'key', 'gender'}
    __mutable__ = {'name', 'description', 'key', 'gender'}
    __unique__ = {'name', 'key'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'name', sqlalchemy.String(64), unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'description', sqlalchemy.String(4096), nullable=False)
    gender: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'gender', sqlalchemy.String(1), nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['CompetitionChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='competition',
        foreign_keys='CompetitionChangeLog.objectFK',
        order_by='desc(CompetitionChangeLog.when)')

    ageCategories: sqlalchemy.orm.Mapped[Set['AgeCategory']] = sqlalchemy.orm.relationship(
        secondary=competitionAgeCategoriesMapping,
        back_populates='competitions',
        order_by='desc(AgeCategory.key)')

    # METHODS ##########################################################################################################
    def eligibleMembers(self, members: List['Member']) -> List['Member']:
        try:
            # check eligibility for each associated age category
            eligibleMembers = [member for member in members if member.eligibleForCompetition(self)]

            # check the gender restriction and return list
            if self.gender == 'A':
                return eligibleMembers
            else:
                return list(filter(lambda member: member.gender.casefold() == self.gender.casefold(), eligibleMembers))

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Competition.getEligibleMembers: {e}')

    def addAgeCategory(self, ageCategory: 'AgeCategory') -> None:
        try:
            if ageCategory not in self.ageCategories:
                self.ageCategories.add(ageCategory)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Competition.addAgeCategory: {e}')

    def removeAgeCategory(self, ageCategory: 'AgeCategory') -> None:
        try:
            if ageCategory in self.ageCategories:
                self.ageCategories.remove(ageCategory)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Competition.removeAgeCategory: {e}')

    # OVERRIDES ########################################################################################################
    def viewPayload(self, sort: bool = True):
        payload = super().viewPayload(sort=False)
        payload.append(
            {
                'key': 'ageCategories',
                'lux': 'Alterskategorien',
                'position': 5,
                'value': sorted(list(self.ageCategories), key=lambda cat: cat.ageMin, reverse=False)
            }
        )
        return sorted(payload, key=lambda pos: pos['position'] if pos['position'] is not None else 0)

    def __repr__(self) -> str:
        return f'{self.name}'
