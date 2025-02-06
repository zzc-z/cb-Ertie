"""
DB Model for Sponsors

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
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
from app.models.searchableMixin import SearchableMixin
from app.models.sponsoring.sponsors.sponsorLuxNames import luxNames
from app.models.sponsoring import sponsorOptionsMapping
from app.models.sponsoring.sponsors.sponsorChangeLog import SponsorChangeLog

# TYPE HINTS ###########################################################################################################
from typing import List, TYPE_CHECKING, Set, Optional

if TYPE_CHECKING:
    from app.models.sponsoring.options.option import Option
    from app.models.members.members.member import Member
    from app.models.addresses.address import Address


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Sponsor(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'sponsor'

    # TRACK CHANGES ####################################################################################################
    __columns__ = {'memberFK', 'lastPayment', 'name', 'lastInvoice', 'anonymous', 'donation'}
    __required__ = {'memberFK', 'name', 'anonymous'}
    __mutable__ = {'memberFK', 'lastPayment', 'name', 'lastInvoice', 'anonymous', 'donation'}
    __unique__ = {'name'}
    __luxNames__ = luxNames

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['name']

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(
        'member_fk', sqlalchemy.Integer, sqlalchemy.ForeignKey('member.uid'))
    name = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64), unique=True, nullable=False)
    donation = sqlalchemy.orm.mapped_column('donation', sqlalchemy.Float, default=0)
    lastPayment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'last_payment', sqlalchemy.Date)
    lastInvoice: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column(
        'last_invoice', sqlalchemy.Date)
    anonymous: sqlalchemy.orm.Mapped[bool] = sqlalchemy.orm.mapped_column('anonymous', sqlalchemy.Boolean,
                                                                          nullable=False)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['SponsorChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='sponsor',
        foreign_keys='SponsorChangeLog.objectFK',
        order_by='desc(SponsorChangeLog.when)')

    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='sponsor')
    address: sqlalchemy.orm.Mapped[Optional['Address']] = sqlalchemy.orm.relationship(back_populates='sponsor',
                                                                                      foreign_keys='Address.sponsorFK')
    options: sqlalchemy.orm.Mapped[Set['Option']] = sqlalchemy.orm.relationship(secondary=sponsorOptionsMapping,
                                                                                back_populates='sponsors',
                                                                                order_by='desc(Option.value)')

    # METHODS ##########################################################################################################
    def addOption(self, option: 'Option') -> None:
        try:
            if option not in self.options and option.available():
                self.options.add(option)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Sponsor.addOption: {e}')

    def removeOption(self, option: 'Option') -> None:
        try:
            if option in self.options:
                self.options.remove(option)
                database.commitFlush()
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Sponsor.removeOption: {e}')

    # OVERRIDES ########################################################################################################
    def canBeDeleted(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'{self.name}'
