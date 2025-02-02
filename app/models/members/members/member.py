"""
DB model for physical people / members / users

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# FLASK & PYTHON #######################################################################################################
from datetime import datetime, timezone, date
from dateutil.relativedelta import relativedelta
from app.factory.extensions import loginManager

# DB & MODELS ##########################################################################################################
from flask_login import UserMixin
import sqlalchemy.orm
from sqlalchemy.dialects import postgresql
from app.factory.extensions import database
from app.factory.extensions.custom.inputValidator import inputValidator
from app.models.members.membersBoardElection import MemberBoardElection
from app.models.members.membersClubMembership.memberClubMembership import MemberClubMembership
from app.models.members.membersAssociationAffiliation.memberAssociationAffiliation import MemberAssociationAffiliation
from app.models.searchableMixin import SearchableMixin
from app.models.addresses import Address
from app.models.sponsoring.sponsors.sponsor import Sponsor
from app.models.mutableMixin import MutableMixin
from app.models.members.members.memberLuxNames import luxNames, luxNamesRoles
from app.models.sports import practiceCoachesMapping
from app.models.sports import practicePlayersMapping

# TYPE HINTS ###########################################################################################################
from typing import List, Set, Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.members import MemberChangeLog
    from app.models.association.ageCategories.ageCategory import AgeCategory
    from app.models.association.competitions.competition import Competition
    from app.models.sports.practiceSessions.practiceSession import PracticeSession
    from app.models.club.practiceTypes.practiceType import PracticeType

########################################################################################################################
# MAPPING ##############################################################################################################
########################################################################################################################
# map users to roles in a many-to-many relationship
roleUserMapping = sqlalchemy.Table('mapping_roles_users', database.db.metadata,
                                   sqlalchemy.Column('member_fk', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey('member.uid'), primary_key=True),
                                   sqlalchemy.Column('role_fk', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey('role.uid'), primary_key=True))


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Member(MutableMixin, UserMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['username', 'givenName', 'familyName', 'email', 'nickname']

    # MUTABLE ##########################################################################################################
    __columns__ = {'authID', 'username', 'givenName', 'familyName', 'email',
                   'nickname', 'gender', 'picture', 'lastLogin', 'lastSeen'}
    __required__ = {'givenName', 'familyName', 'email', 'gender'}
    __mutable__ = {'username', 'givenName', 'familyName', 'email', 'nickname',
                   'gender', 'picture', 'lastLogin', 'lastSeen'}
    __unique__ = {'username'}
    __uniqueTuples__ = {('givenName', 'familyName')}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    authID: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('auth_id',
                                                                                postgresql.BIGINT)
    username: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('username',
                                                                                  sqlalchemy.String(64), unique=True)
    givenName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('given_name',
                                                                         sqlalchemy.String(64), nullable=False)
    familyName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('family_name',
                                                                          sqlalchemy.String(64), nullable=False)
    email: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('email',
                                                                     sqlalchemy.String(128), nullable=False)
    nickname: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('nickname',
                                                                                  sqlalchemy.String(64))
    gender: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('gender',
                                                                      sqlalchemy.String(1), nullable=False)
    picture: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('picture',
                                                                                 sqlalchemy.String(4096))
    lastLogin: sqlalchemy.orm.Mapped[Optional[datetime]] = sqlalchemy.orm.mapped_column('last_login',
                                                                                        postgresql.types.TIMESTAMP(
                                                                                            timezone=True))
    lastSeen: sqlalchemy.orm.Mapped[Optional[datetime]] = sqlalchemy.orm.mapped_column('last_seen',
                                                                                       postgresql.types.TIMESTAMP(
                                                                                           timezone=True))

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List[MemberChangeLog]] = sqlalchemy.orm.relationship(
        back_populates='member', foreign_keys='MemberChangeLog.objectFK', order_by='desc(MemberChangeLog.when)')

    roles: sqlalchemy.orm.Mapped[Set[Role]] = sqlalchemy.orm.relationship(secondary=roleUserMapping,
                                                                          back_populates='users')

    address: sqlalchemy.orm.Mapped[Optional[Address]] = sqlalchemy.orm.relationship(back_populates='member',
                                                                                    foreign_keys='Address.memberFK')
    sponsor: sqlalchemy.orm.Mapped[Optional[Sponsor]] = sqlalchemy.orm.relationship(back_populates='member',
                                                                                    foreign_keys='Sponsor.memberFK')

    clubMembership: sqlalchemy.orm.Mapped[Optional[MemberClubMembership]] = sqlalchemy.orm.relationship(
        back_populates='member',
        foreign_keys='MemberClubMembership.memberFK')

    boardElection: sqlalchemy.orm.Mapped[Optional[MemberBoardElection]] = sqlalchemy.orm.relationship(
        back_populates='member',
        foreign_keys='MemberBoardElection.memberFK'
    )

    associationAffiliation: sqlalchemy.orm.Mapped[Optional[MemberAssociationAffiliation]] = sqlalchemy.orm.relationship(
        back_populates='member',
        foreign_keys='MemberAssociationAffiliation.memberFK'
    )

    practiceSessionsAsPlayer: sqlalchemy.orm.Mapped[Set['PracticeSession']] = sqlalchemy.orm.relationship(
        secondary=practicePlayersMapping,
        back_populates='players')

    practiceSessionsAsCoach: sqlalchemy.orm.Mapped[Set['PracticeSession']] = sqlalchemy.orm.relationship(
        secondary=practiceCoachesMapping,
        back_populates='coaches')

    # METHODS ##########################################################################################################
    def checkAge(self, ageToCheck: int, deadline: date, leq: bool = False, mode: str = 'min') -> bool:
        try:
            inputValidator.positiveInteger(ageToCheck, allowZero=True)
            inputValidator.string(mode, allowed={'min', 'max'})

            if not self.clubMembership:
                return False

            # construct relative date and compute hypothetical age
            relativeDate = date.today()
            relativeDate = relativeDate.replace(year=relativeDate.year, month=deadline.month, day=deadline.day)
            age = relativedelta(relativeDate, self.clubMembership.birthday).years

            # return age check based on whether we are in competition or age category type
            if leq:
                return ageToCheck <= age if mode == 'min' else age <= ageToCheck
            else:
                return ageToCheck <= age if mode == 'min' else age < ageToCheck

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.checkAge: {e}')

    def eligibleForAgeCategory(self, ageCategory: 'AgeCategory', leqMax: bool = False, leqMin: bool = False) -> bool:
        try:
            if not self.clubMembership and not self.associationAffiliation:
                return False

            # match all age criteria
            return all([self.checkAge(ageCategory.ageMin, ageCategory.deadlineMin, leq=leqMin, mode='min'),
                        self.checkAge(ageCategory.ageMax, ageCategory.deadlineMax, leq=leqMax, mode='max')])

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.inAgeCategory: {e}')

    def eligibleAgeCategories(self, ageCategories: List['AgeCategory']) -> List['AgeCategory']:
        try:
            return [ageCategory for ageCategory in ageCategories if self.eligibleForAgeCategory(ageCategory)]

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligibleAgeCategories: {e}')

    def eligibleForCompetition(self, competition: 'Competition') -> bool:
        try:
            if not self.clubMembership and not self.associationAffiliation:
                return False

            # match any age criteria as well as the gender criteria
            return (any([self.eligibleForAgeCategory(ageCategory, leqMax=True)
                         for ageCategory in competition.ageCategories])
                    and self.gender.casefold() == competition.gender.casefold()) if competition.gender != 'A' else True

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligibleForCompetition: {e}')

    def eligibleCompetitions(self, competitions: List['Competition']) -> List['Competition']:
        try:
            return [competition for competition in competitions if self.eligibleForCompetition(competition)]

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligibleCompetitions: {e}')

    def eligibleAgeCategoriesAndCompetitions(self, ageCategories: List['AgeCategory'],
                                             competitions: List['Competition']) \
            -> Tuple[List['AgeCategory'], List['Competition']]:
        try:
            return self.eligibleAgeCategories(ageCategories), self.eligibleCompetitions(competitions)

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligibleAgeCategoriesAndCompetitions: {e}')

    def eligibleForPracticeType(self, practiceType: 'PracticeType') -> bool:
        try:
            if not self.clubMembership and not self.associationAffiliation:
                return False

            # match all age criteria as well as the gender criteria
            return (any([self.eligibleForAgeCategory(ageCategory, leqMax=True)
                         for ageCategory in practiceType.ageCategories])
                    and self.gender.casefold() == practiceType.gender.casefold()) \
                if practiceType.gender != 'A' else True

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligibleForPracticeType: {e}')

    def eligiblePracticeTypes(self, practiceTypes: List['PracticeType']) -> List['PracticeType']:
        try:
            return [practiceType for practiceType in practiceTypes if self.eligibleForPracticeType(practiceType)]

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.eligiblePracticeTypes: {e}')

    def hasRoles(self, necessaryRoles: List[str] | Set[str], allNecessary: bool = False) -> bool:
        try:
            inputValidator.boolean(allNecessary)

            # check user roles -> convert roles into a set for fast intersection check
            userRoles = {role.key for role in self.roles}
            if not userRoles:
                # the user has no roles
                return False

            # check roles via set intersection
            roleMatches = userRoles.intersection(necessaryRoles)

            if allNecessary:
                # ensure that the user has all the necessary roles
                return len(roleMatches) == len(necessaryRoles)
            else:
                # check if at least one role was a match
                return bool(roleMatches)

        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.hasRoles: {e}')

    def hasRole(self, roleKey: str) -> bool:
        try:
            inputValidator.string(roleKey)

            if not self.roles:
                # the user has no roles at all
                return False

            return any(roleKey == role.key for role in self.roles)
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Member.hasRole {e}')

    def getTime(self, tz: str = 'UTC', mode: str = 'lastLogin') -> datetime:
        try:
            inputValidator.string(tz)
            match mode:
                case 'lastLogin':
                    return self.lastLogin.astimezone(timezone.utc)
                case 'lastSeen':
                    return self.lastSeen.astimezone(timezone.utc)
                case _:
                    raise ValueError(f'Invalid Mode @ Member.getTime: {mode}')

        except Exception as e:
            raise RuntimeError(f'Unexpected Error @ Member.getTime: {e}')

    # OVERRIDES ########################################################################################################
    def get_id(self) -> int:
        return self.uid

    def __repr__(self) -> str:
        return f'{self.givenName} {self.familyName}'

    def canBeDeleted(self) -> bool:
        try:
            if self.clubMembership and self.clubMembership.active:
                return False
            return True

        except Exception as e:
            raise RuntimeError(f'Unexpected Error @ Member.canBeDeleted: {e}')


class Role(MutableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'role'

    # MUTABLE ##########################################################################################################
    __columns__ = {'key', 'name', 'description'}
    __required__ = {'key', 'name', 'description'}
    __mutable__ = {'description'}
    __unique__ = {'key', 'name', 'description'}
    __luxNames__ = luxNamesRoles

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096),
                                                                           unique=True, nullable=False)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(64),
                                                                   unique=True, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    users: sqlalchemy.orm.Mapped[Set[Member]] = sqlalchemy.orm.relationship(secondary=roleUserMapping,
                                                                            back_populates='roles')

    # METHODS ##########################################################################################################
    def addUser(self, user: Member) -> None:
        try:
            if not isinstance(user, Member):
                raise TypeError(f'Type Error @ Role.addUser ; expected: Member ; received: {type(user)}')

            if user not in self.users:
                self.users.add(user)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Role.addUser: {e}')

    def removeUser(self, user: Member) -> None:
        if not isinstance(user, Member):
            raise TypeError(f'Type Error @ Role.removeUser ; expected: Member ; received: {type(user)}')

        try:
            if user in self.users:
                self.users.remove(user)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Role.removeUser: {e}')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self):
        # do not delete roles with associated users
        return len(self.users) == 0

    def __repr__(self) -> str:
        return f'{self.name}'


# PUBLIC METHODS #######################################################################################################
@loginManager.user_loader
def loadUser(userID: int) -> Member:
    try:
        inputValidator.positiveInteger(userID)
        user = Member.query.get(userID)
        if not user:
            raise LookupError(f'Lookup Error @bpAuth.loadUser: User with ID {userID} not found!')
        return user
    except Exception as e:
        raise RuntimeError(f'Runtime Error @ bpAuth.loadUser: {e}')
