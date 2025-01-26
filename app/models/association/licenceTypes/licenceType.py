"""
DB Model for Licence Types

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
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
from app.models.association.licenceTypes.licenceTypeLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.association.licenceTypes.licenceTypeChangeLog import LicenceTypeChangeLog
    from app.models.members.membersAssociationAffiliation import MemberAssociationAffiliation


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class LicenceType(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'association_licence_type'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['key', 'name', 'description', 'fee']

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'key', 'name', 'description', 'fee'}
    __required__ = {'key', 'name', 'description', 'fee'}
    __mutable__ = {'key', 'name', 'description', 'fee'}
    __unique__ = {'key', 'name', 'description'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('key', sqlalchemy.String(32),
                                                                   unique=True, nullable=False)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True, nullable=False)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        'description', sqlalchemy.String(4096), unique=True, nullable=False)
    fee: sqlalchemy.orm.Mapped[float] = sqlalchemy.orm.mapped_column('fee', sqlalchemy.Float, nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['LicenceTypeChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='licenceType',
        foreign_keys='LicenceTypeChangeLog.objectFK',
        order_by='desc(LicenceTypeChangeLog.when)')

    memberAffiliations: sqlalchemy.orm.Mapped[
        Optional[List['MemberAssociationAffiliation']]] = sqlalchemy.orm.relationship(
        back_populates='licenceType', foreign_keys='MemberAssociationAffiliation.associationLicenceTypeFK')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return len(self.memberAffiliations) == 0

    def __repr__(self) -> str:
        return f'{self.name}'
