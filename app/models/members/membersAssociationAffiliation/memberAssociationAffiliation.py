"""
DB Model for Member Association Affiliations

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# FLASK & PYTHON #######################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
from flask_login import UserMixin
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.mutableMixin import MutableMixin
from app.models.searchableMixin import SearchableMixin
from app.models.members.membersAssociationAffiliation.memberAssociationAffiliationChangeLog import \
    MemberAssociationAffiliationChangeLog
from app.models.association.competitions import Competition

# HELPERS ##############################################################################################################
from app.models.members.membersAssociationAffiliation.memberAssociationAffiliationLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.members import Member
    from app.models.association.licenceTypes import LicenceType
    from app.models.association.ageCategories.ageCategory import AgeCategory


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberAssociationAffiliation(MutableMixin, UserMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_association_affiliation'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['associationLicenceNumber']

    # MUTABLE ##########################################################################################################
    __columns__ = {'memberFK', 'associationLicenceTypeFK', 'associationLicenceNumber', 'joined', 'left'}
    __required__ = {'memberFK', 'associationLicenceTypeFK', 'associationLicenceNumber'}
    __mutable__ = {'associationLicenceTypeFK', 'associationLicenceNumber', 'joined', 'left'}
    __unique__ = {'memberFK', 'associationLicenceNumber'}
    __uniqueTuples__ = {}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)

    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk', sqlalchemy.Integer,
                                                                        sqlalchemy.ForeignKey('member.uid'),
                                                                        nullable=False)
    associationLicenceTypeFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'association_licence_type_fk', sqlalchemy.Integer,
        sqlalchemy.ForeignKey('association_licence_type.uid'), nullable=False)

    associationLicenceNumber: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'association_licence_number', sqlalchemy.String(32), nullable=False)
    joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('joined',
                                                                                 sqlalchemy.Date)
    left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('left', sqlalchemy.Date)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List[MemberAssociationAffiliationChangeLog]] = sqlalchemy.orm.relationship(
        back_populates='memberAssociationAffiliation',
        foreign_keys='MemberAssociationAffiliationChangeLog.objectFK',
        order_by='desc(MemberAssociationAffiliationChangeLog.when)')

    licenceType: sqlalchemy.orm.Mapped['LicenceType'] = sqlalchemy.orm.relationship(back_populates='memberAffiliations')
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='associationAffiliation')

    # METHODS ##########################################################################################################
    def viewPayload(self, ageCategories: List['AgeCategory'] = None, competitions: List[Competition] = None):
        try:
            payload = super().viewPayload()

            if ageCategories is None and competitions is None:
                return payload

            # check available age categories and competitions based on age and gender criteria
            if self.member.clubMembership is not None:
                ageCategories, competitions = self.member.eligibleAgeCategoriesAndCompetitions(
                    ageCategories, competitions)

                payload.append({'key': 'ageCategories', 'value': ageCategories, 'lux': 'Alterskategorien'})
                payload.append({'key': 'competitions', 'value': competitions, 'lux': 'Kompetitiounen'})

            return payload
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberAssociationAffiliation: {e}') from e

    def canBeDeleted(self) -> bool:
        try:
            return True if self.left else False
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ MemberAssociationAffiliation: {e}') from e

    def __repr__(self) -> str:
        return f'{self.member} ({self.associationLicenceNumber})'
