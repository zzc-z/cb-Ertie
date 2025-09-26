"""
DB model for the changelog of invoices.

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
from app.models.changeLogMixing import ChangeLogMixin

# HELPERS ##############################################################################################################
from app.models.invoices.invoiceLuxNames import luxNames

# TYPE HINTS ###########################################################################################################
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.invoices import Invoice

########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################
class InvoiceChangeLog(ChangeLogMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'invoice_changelog'

    # TRACKED FIELDS ###################################################################################################
    __trackedFields__ = {'number', 'date', 'payment'}
    __luxNames__ = luxNames

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    objectFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('object_fk',
                                                                        sqlalchemy.ForeignKey('invoice.uid'),
                                                                        index=True, nullable=False)
    new_number: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_number',
                                                                                         sqlalchemy.String(16))
    new_date: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_date',
                                                                                    sqlalchemy.Date)
    new_payment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('new_payment',
                                                                                      sqlalchemy.Date)
    old_number: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_number',
                                                                                         sqlalchemy.String(12))
    old_date: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_date',
                                                                                    sqlalchemy.Date)
    old_payment: sqlalchemy.orm.Mapped[Optional[date]] = sqlalchemy.orm.mapped_column('old_payment',
                                                                                    sqlalchemy.Date)


    # RELATIONSHIPS ####################################################################################################
    invoice: sqlalchemy.orm.Mapped['Invoice'] = sqlalchemy.orm.relationship(back_populates='history',
                                                                            foreign_keys='InvoiceChangeLog.objectFK')
