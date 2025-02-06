"""
DB Model for Practice Types

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.searchableMixin import SearchableMixin
from app.models.club.practiceTypes.practiceTypeLuxNames import luxNames
from app.models.club import practiceTypeAgeCategoriesMapping
from app.models.sports.practiceSessions.practiceSession import PracticeSession

# TYPE HINTS ###########################################################################################################
from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.club.practiceTypes.practiceTypeChangeLog import PracticeTypeChangeLog
    from app.models.association.ageCategories.ageCategory import AgeCategory
    from app.models.members.members.member import Member


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class PracticeType(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'club_practice_type'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'gender', 'description'}
    __required__ = {'key', 'name', 'gender', 'description'}
    __mutable__ = {'key', 'name', 'gender', 'description'}
    __unique__ = {'key', 'name', 'description'}
    __luxNames__ = luxNames

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description']

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096),
                                                                           unique=True, nullable=False)
    gender: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('gender', sqlalchemy.String(1),
                                                                      nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['PracticeTypeChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='practiceType',
        foreign_keys='PracticeTypeChangeLog.objectFK',
        order_by='desc(PracticeTypeChangeLog.when)')

    practiceSessions: sqlalchemy.orm.Mapped[List['PracticeSession']] = sqlalchemy.orm.relationship(
        back_populates='practiceType',
        order_by='desc(PracticeSession.date)')

    ageCategories: sqlalchemy.orm.Mapped[Set['AgeCategory']] = sqlalchemy.orm.relationship(
        secondary=practiceTypeAgeCategoriesMapping,
        back_populates='practiceTypes',
        order_by='desc(AgeCategory.key)')

    # METHODS ##########################################################################################################
    def eligibleMembers(self, members: List['Member']) -> List['Member']:
        try:
            # check eligibility for each associated age category
            eligibleMembers = [member for member in members if member.eligibleForPracticeType(self)]

            # check the gender restriction and return list
            if self.gender == 'A':
                return eligibleMembers
            else:
                return list(filter(lambda member: member.gender.casefold() == self.gender.casefold(), eligibleMembers))

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeType.getEligibleMembers: {e}')

    def addAgeCategory(self, ageCategory: 'AgeCategory') -> None:
        try:
            if ageCategory not in self.ageCategories:
                self.ageCategories.add(ageCategory)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeType.addAgeCategory: {e}')

    def removeAgeCategory(self, ageCategory: 'AgeCategory') -> None:
        try:
            if ageCategory in self.ageCategories:
                self.ageCategories.remove(ageCategory)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ PracticeType.removeAgeCategory: {e}')

    # OVERRIDES ########################################################################################################
    def viewPayload(self, sort: bool = True):
        payload = super().viewPayload(sort=False)
        payload.append(
            {
                'key': 'ageCategories',
                'lux': 'Alterskategorien',
                'position': 3,
                'value': sorted(list(self.ageCategories), key=lambda cat: cat.ageMin, reverse=False)
            }
        )
        return sorted(payload, key=lambda pos: pos['position'] if pos['position'] is not None else 0)

    def canBeDeleted(self) -> bool:
        # do not delete training types with active practice sessions
        return len(self.practiceSessions) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
