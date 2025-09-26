"""
DB model for invoices

SPDX-FileCopyrightText: © 2024 Gilles Bellot <licence@sl.bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from __future__ import annotations

# PYTHON ###############################################################################################################
from datetime import date

# DB & MODELS ##########################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database
from app.models.searchableMixin import SearchableMixin
from app.models.mutableMixin import MutableMixin

# TYPE HINTS ###########################################################################################################
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.invoices.invoiceChangeLog import InvoiceChangeLog
    from app.models.members.members import Member
    from app.models.sponsoring.sponsors import Sponsor

# HELPERS ##############################################################################################################
from app.models.invoices.invoiceLuxNames import luxNames


########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class Invoice(MutableMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'invoice'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['number']

    # MUTABLE ##########################################################################################################
    __columns__ = {'number', 'date', 'payment', 'memberFK', 'sponsorFK'}
    __required__ = {'number', 'date'}
    __mutable__ = {'number', 'date', 'payment'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('member_fk',
                                                                                  sqlalchemy.ForeignKey('member.uid'),
                                                                                  index=True)
    sponsorFK: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column('sponsor_fk',
                                                                                   sqlalchemy.ForeignKey('sponsor.uid'),
                                                                                   index=True)

    number: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('number',
                                                                           sqlalchemy.String(16),
                                                                           default='', nullable=False)
    date: sqlalchemy.orm.Mapped[date] = sqlalchemy.orm.mapped_column('date',
                                                                      sqlalchemy.Date, default=date.today())
    payment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('payment',
                                                                                      sqlalchemy.Date)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['InvoiceChangeLog']] = sqlalchemy.orm.relationship(
        back_populates='invoice', foreign_keys='InvoiceChangeLog.objectFK', order_by='desc(InvoiceChangeLog.when)')
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='invoices')
    sponsor: sqlalchemy.orm.Mapped['Sponsor'] = sqlalchemy.orm.relationship(back_populates='invoices')

    # OVERRIDES ########################################################################################################
    def __repr__(self) -> str:
        try:
            if self.member is not None:
                return f'Invoice #{self.number} @ {self.member.givenName} {self.member.familyName}'
            else:
                return f'Invoice #{self.number} @ {self.sponsor.name}'
        except Exception as e:
            raise RuntimeError(f'Runtime Error @ Invoice.__repr__: {e}')
