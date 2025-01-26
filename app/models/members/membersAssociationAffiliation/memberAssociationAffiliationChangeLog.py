"""
DB Changelog Model for Member Association Affiliations

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
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation

# HELPERS ##############################################################################################################
from app.models.members.membersAssociationAffiliation.memberAssociationAffiliationLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class MemberAssociationAffiliationChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_association_affiliation_changelog'

    # TRACKED FIELDS ###################################################################################################
    __trackedFields__ = {'associationLicenceTypeFK', 'associationLicenceNumber', 'joined', 'left'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        'object_fk', sqlalchemy.ForeignKey('member_association_affiliation.uid'), index=True, nullable=False)

    new_associationLicenceTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'new_association_licence_type_fk', sqlalchemy.Integer)
    new_associationLicenceNumber: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'new_association_licence_number', sqlalchemy.String(64))
    new_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_joined', sqlalchemy.Date)
    new_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'new_left', sqlalchemy.Date)

    old_associationLicenceTypeFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'old_association_licence_type_fk', sqlalchemy.Integer)
    old_associationLicenceNumber: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(
        'old_association_licence_number', sqlalchemy.String(64))
    old_joined: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_joined', sqlalchemy.Date)
    old_left: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'old_left', sqlalchemy.Date)

    # RELATIONSHIPS ####################################################################################################
    memberAssociationAffiliation: sqlalchemy.orm.Mapped['MemberAssociationAffiliation'] = sqlalchemy.orm.relationship(
        back_populates='history', foreign_keys='MemberAssociationAffiliationChangeLog.objectFK')
